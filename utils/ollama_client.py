"""
Ollama client for AI translation models
"""
import asyncio
import logging
import json
from typing import Optional, Dict, Any
import httpx
from utils.config import config

logger = logging.getLogger(__name__)

class OllamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, base_url: str = None, timeout: int = None):
        self.base_url = base_url or config.OLLAMA_BASE_URL
        self.timeout = timeout or config.OLLAMA_TIMEOUT
        self.client = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.client:
            await self.client.aclose()
    
    async def is_available(self) -> bool:
        """Check if Ollama service is available"""
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama service not available: {e}")
            return False
    
    async def list_models(self) -> list:
        """List available models in Ollama"""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    data = response.json()
                    return [model['name'] for model in data.get('models', [])]
                return []
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []
    
    async def pull_model(self, model_name: str) -> bool:
        """Pull/download a model to Ollama"""
        try:
            logger.info(f"Pulling model: {model_name}")
            async with httpx.AsyncClient(timeout=600) as client:  # 10 minutes timeout
                async with client.stream('POST', f"{self.base_url}/api/pull", 
                                       json={'name': model_name}) as response:
                    if response.status_code == 200:
                        async for line in response.aiter_lines():
                            if line.strip():
                                try:
                                    data = json.loads(line)
                                    if 'status' in data:
                                        logger.info(f"Pull status: {data['status']}")
                                except json.JSONDecodeError:
                                    pass
                        logger.info(f"Model {model_name} pulled successfully")
                        return True
            return False
        except Exception as e:
            logger.error(f"Failed to pull model {model_name}: {e}")
            return False
    
    async def translate(self, text: str, source_lang: str, target_lang: str, 
                       model_name: str) -> Optional[str]:
        """
        Translate text using Ollama model
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code  
            model_name: Ollama model name
            
        Returns:
            Translated text or None if failed
        """
        try:
            # Create translation prompt
            prompt = self._create_translation_prompt(text, source_lang, target_lang)
            
            # Call Ollama API
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                payload = {
                    'model': model_name,
                    'prompt': prompt,
                    'stream': False,
                    'options': {
                        'temperature': 0.3,  # Lower temperature for more consistent translation
                        'top_p': 0.9,
                        'max_tokens': 1000
                    }
                }
                
                response = await client.post(f"{self.base_url}/api/generate", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    translated_text = data.get('response', '').strip()
                    
                    # Clean up the response
                    translated_text = self._clean_translation_response(translated_text)
                    
                    logger.info(f"Translation completed: {source_lang} -> {target_lang}")
                    return translated_text
                else:
                    logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                    return None
                    
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return None
    
    def _create_translation_prompt(self, text: str, source_lang: str, target_lang: str) -> str:
        """Create translation prompt for Ollama"""
        
        # Language mapping for better prompts
        lang_names = {
            'en': 'English',
            'vi': 'Vietnamese', 
            'ja': 'Japanese',
            'ko': 'Korean',
            'ru': 'Russian',
            'fa': 'Persian',
            'zh': 'Chinese',
            'th': 'Thai',
            'id': 'Indonesian',
            'ms': 'Malay',
            'de': 'German',
            'fr': 'French',
            'es': 'Spanish',
            'it': 'Italian'
        }
        
        source_name = lang_names.get(source_lang, source_lang)
        target_name = lang_names.get(target_lang, target_lang)
        
        prompt = f"""You are a professional translator. Translate the following text from {source_name} to {target_name}.

Text to translate: "{text}"

Translation:"""
        
        return prompt
    
    def _clean_translation_response(self, response: str) -> str:
        """Clean up translation response from Ollama"""
        # Remove common prefixes/suffixes that models might add
        prefixes_to_remove = [
            'Translation:',
            'Translated text:',
            'Here is the translation:',
            'The translation is:'
        ]
        
        response = response.strip()
        
        for prefix in prefixes_to_remove:
            if response.lower().startswith(prefix.lower()):
                response = response[len(prefix):].strip()
        
        # Remove quotes if the entire response is quoted
        if response.startswith('"') and response.endswith('"'):
            response = response[1:-1]
        
        return response.strip()
    
    async def get_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a model"""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(f"{self.base_url}/api/show", 
                                           json={'name': model_name})
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            logger.error(f"Failed to get model info: {e}")
            return None
