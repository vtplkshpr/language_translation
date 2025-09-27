"""
AI-powered local translation using Ollama
"""
import asyncio
import logging
import time
from typing import Optional, Dict, Any, List
from utils.config import config
from utils.ollama_client import OllamaClient
from models.translation_models import TranslationRequest, TranslationCache, ModelInfo
from services.translation_cache import TranslationCacheService
from services.database import DatabaseService

logger = logging.getLogger(__name__)

class AILocalTranslator:
    """AI-powered local translation using Ollama models"""
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or config.DEFAULT_MODEL
        self.cache_service = TranslationCacheService()
        self.db_service = DatabaseService()
        self.ollama_client = None
        
        # Validate model
        if self.model_name not in config.SUPPORTED_MODELS:
            logger.warning(f"Model {self.model_name} not supported, using default")
            self.model_name = config.DEFAULT_MODEL
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.ollama_client = OllamaClient()
        await self.ollama_client.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.ollama_client:
            await self.ollama_client.__aexit__(exc_type, exc_val, exc_tb)
    
    async def translate_text(self, text: str, target_language: str, 
                           source_language: str = 'auto') -> Optional[str]:
        """
        Translate text using local AI model
        
        Args:
            text: Text to translate
            target_language: Target language code
            source_language: Source language code (auto-detect if not provided)
        
        Returns:
            Translated text or None if failed
        """
        if not text or not text.strip():
            return text
        
        # Validate input
        if len(text) > config.MAX_TEXT_LENGTH:
            logger.error(f"Text too long: {len(text)} chars (max: {config.MAX_TEXT_LENGTH})")
            return None
        
        # Detect language if auto
        if source_language == 'auto':
            source_language = await self.detect_language(text)
        
        # Check cache first
        if config.CACHE_ENABLED:
            cached_result = await self.cache_service.get_cached_translation(
                text, source_language, target_language
            )
            if cached_result:
                logger.debug(f"Translation cache hit for: {text[:50]}...")
                return cached_result['translated_text']
        
        # Create translation request record
        request_id = await self._create_translation_request(
            text, source_language, target_language
        )
        
        start_time = time.time()
        
        try:
            # Translate using AI model
            translated_text = await self._perform_translation(
                text, source_language, target_language
            )
            
            processing_time = time.time() - start_time
            
            if translated_text:
                # Update request record
                await self._update_translation_request(
                    request_id, translated_text, 'completed', 
                    processing_time=processing_time
                )
                
                # Cache the result
                if config.CACHE_ENABLED:
                    await self.cache_service.cache_translation(
                        text, source_language, target_language, 
                        translated_text, self.model_name
                    )
                
                logger.info(f"Translation completed: {source_language} -> {target_language} ({processing_time:.2f}s)")
                return translated_text
            else:
                # Update request record with failure
                await self._update_translation_request(
                    request_id, None, 'failed', 
                    processing_time=processing_time,
                    error_message="Translation failed"
                )
                return None
                
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"Translation failed: {e}")
            
            # Update request record with error
            await self._update_translation_request(
                request_id, None, 'failed',
                processing_time=processing_time,
                error_message=str(e)
            )
            return None
    
    async def translate_to_all_languages(self, text: str, 
                                       source_language: str = 'auto') -> Dict[str, str]:
        """
        Translate text to all supported languages
        
        Args:
            text: Text to translate
            source_language: Source language code
        
        Returns:
            Dictionary mapping language codes to translated text
        """
        translations = {}
        supported_languages = config.get_supported_languages(self.model_name)
        
        # Create semaphore to limit concurrent translations
        semaphore = asyncio.Semaphore(config.MAX_CONCURRENT_TRANSLATIONS)
        
        async def translate_language(target_lang: str):
            async with semaphore:
                if target_lang == source_language:
                    return target_lang, text
                
                translated = await self.translate_text(text, target_lang, source_language)
                return target_lang, translated or text  # Fallback to original if failed
        
        # Create tasks for all languages
        tasks = [translate_language(lang) for lang in supported_languages]
        
        # Execute translations concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Translation task failed: {result}")
            else:
                lang, translated_text = result
                translations[lang] = translated_text
        
        return translations
    
    async def detect_language(self, text: str) -> str:
        """
        Detect language of text using AI model
        
        Args:
            text: Text to analyze
        
        Returns:
            Detected language code
        """
        if not text or not text.strip():
            return 'auto'
        
        try:
            # Simple language detection based on character sets
            if any('\u4e00' <= char <= '\u9fff' for char in text):  # Chinese/Japanese
                return 'ja'
            elif any('\uac00' <= char <= '\ud7af' for char in text):  # Korean
                return 'ko'
            elif any('\u0400' <= char <= '\u04ff' for char in text):  # Cyrillic
                return 'ru'
            elif any('\u0600' <= char <= '\u06ff' for char in text):  # Arabic/Persian
                return 'fa'
            elif any('\u0e00' <= char <= '\u0e7f' for char in text):  # Thai
                return 'th'
            elif any('\u4e00' <= char <= '\u9fff' for char in text):  # Chinese
                return 'zh'
            else:
                # Default to English for Latin script
                return 'en'
                
        except Exception as e:
            logger.error(f"Language detection failed: {e}")
            return 'en'
    
    async def get_supported_languages(self) -> Dict[str, str]:
        """Get supported languages with their names"""
        return config.LANGUAGE_NAMES.copy()
    
    async def get_model_info(self) -> Dict[str, Any]:
        """Get information about current model"""
        model_config = config.get_model_config(self.model_name)
        
        # Check if model is available in Ollama
        is_available = False
        if self.ollama_client:
            available_models = await self.ollama_client.list_models()
            is_available = self.model_name in available_models
        
        return {
            'name': self.model_name,
            'config': model_config,
            'is_available': is_available,
            'supported_languages': model_config['languages']
        }
    
    async def _perform_translation(self, text: str, source_lang: str, 
                                 target_lang: str) -> Optional[str]:
        """Perform actual translation using Ollama"""
        if not self.ollama_client:
            raise RuntimeError("Ollama client not initialized")
        
        return await self.ollama_client.translate(
            text, source_lang, target_lang, self.model_name
        )
    
    async def _create_translation_request(self, text: str, source_lang: str, 
                                        target_lang: str) -> int:
        """Create translation request record in database"""
        try:
            async with self.db_service.get_session() as session:
                request = TranslationRequest(
                    source_text=text,
                    source_language=source_lang,
                    target_language=target_lang,
                    model_used=self.model_name,
                    status='processing'
                )
                session.add(request)
                await session.commit()
                return request.id
        except Exception as e:
            logger.error(f"Failed to create translation request: {e}")
            return 0
    
    async def _update_translation_request(self, request_id: int, translated_text: str = None,
                                        status: str = None, processing_time: float = None,
                                        error_message: str = None):
        """Update translation request record"""
        try:
            async with self.db_service.get_session() as session:
                request = await session.get(TranslationRequest, request_id)
                if request:
                    if translated_text is not None:
                        request.translated_text = translated_text
                    if status is not None:
                        request.status = status
                    if processing_time is not None:
                        request.processing_time = processing_time
                    if error_message is not None:
                        request.error_message = error_message
                    
                    await session.commit()
        except Exception as e:
            logger.error(f"Failed to update translation request: {e}")
    
    async def batch_translate(self, texts: List[str], target_language: str, 
                            source_language: str = 'auto') -> List[Optional[str]]:
        """
        Translate multiple texts in batch
        
        Args:
            texts: List of texts to translate
            target_language: Target language code
            source_language: Source language code
        
        Returns:
            List of translated texts
        """
        # Limit concurrent translations
        semaphore = asyncio.Semaphore(config.MAX_CONCURRENT_TRANSLATIONS)
        
        async def translate_single(text: str):
            async with semaphore:
                return await self.translate_text(text, target_language, source_language)
        
        # Create tasks
        tasks = [translate_single(text) for text in texts]
        
        # Execute translations
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Batch translation failed: {result}")
                processed_results.append(None)
            else:
                processed_results.append(result)
        
        return processed_results
