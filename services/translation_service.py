"""
Main translation service for language translation ability
"""
import logging
from typing import Optional, Dict, Any, List
from core.ai_translator import AILocalTranslator
from utils.config import config
from services.database import db_service

logger = logging.getLogger(__name__)

class TranslationService:
    """Main translation service using AI local models"""
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or config.DEFAULT_MODEL
        self.translator = None
        self._initialized = False
    
    async def initialize(self):
        """Initialize the translation service"""
        if self._initialized:
            return
        
        try:
            # Test database connection
            if not await db_service.test_connection():
                logger.error("Database connection failed")
                return False
            
            # Initialize AI translator
            self.translator = AILocalTranslator(self.model_name)
            await self.translator.__aenter__()
            
            # Check if Ollama is available
            if not await self.translator.ollama_client.is_available():
                logger.error("Ollama service not available")
                return False
            
            self._initialized = True
            logger.info(f"Translation service initialized with model: {self.model_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize translation service: {e}")
            return False
    
    async def translate_text(self, text: str, target_language: str, 
                           source_language: str = 'auto') -> Optional[str]:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_language: Target language code
            source_language: Source language code (auto-detect if not provided)
        
        Returns:
            Translated text or None if failed
        """
        if not self._initialized:
            if not await self.initialize():
                return None
        
        return await self.translator.translate_text(text, target_language, source_language)
    
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
        if not self._initialized:
            if not await self.initialize():
                return {}
        
        return await self.translator.translate_to_all_languages(text, source_language)
    
    async def detect_language(self, text: str) -> str:
        """
        Detect language of text
        
        Args:
            text: Text to analyze
        
        Returns:
            Detected language code
        """
        if not self._initialized:
            if not await self.initialize():
                return 'auto'
        
        return await self.translator.detect_language(text)
    
    async def get_supported_languages(self) -> Dict[str, str]:
        """Get supported languages with their names"""
        return await self.translator.get_supported_languages()
    
    async def get_model_info(self) -> Dict[str, Any]:
        """Get information about current model"""
        if not self._initialized:
            if not await self.initialize():
                return {}
        
        return await self.translator.get_model_info()
    
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
        if not self._initialized:
            if not await self.initialize():
                return [None] * len(texts)
        
        return await self.translator.batch_translate(texts, target_language, source_language)
    
    async def close(self):
        """Close the translation service"""
        if self.translator:
            await self.translator.__aexit__(None, None, None)
            self.translator = None
        
        self._initialized = False
        logger.info("Translation service closed")

# Global translation service instance
translation_service = TranslationService()
