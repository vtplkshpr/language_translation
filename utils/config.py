"""
Configuration for Language Translation Ability
"""
import os
from typing import Dict, List, Any
from dotenv import load_dotenv

# Load environment variables from .env file
# Try to load from multiple locations
load_dotenv()  # Current directory
load_dotenv('.env')  # Explicit .env file
load_dotenv('../.env')  # Parent directory
load_dotenv('../../.env')  # Root directory

class TranslationConfig:
    """Configuration class for AI translation service"""
    
    # Ollama Configuration
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    OLLAMA_TIMEOUT = int(os.getenv('OLLAMA_TIMEOUT', '300'))  # 5 minutes
    
    # Supported AI Models
    SUPPORTED_MODELS = {
        'llama2': {
            'name': 'llama2:latest',
            'provider': 'ollama',
            'size': '3.8GB',
            'languages': ['en', 'vi', 'ja', 'ko', 'ru', 'fa', 'zh', 'th', 'id', 'ms', 'de', 'fr', 'es', 'it'],
            'description': 'Meta Llama2 model - High quality general purpose model for translation'
        },
        'nllb-200': {
            'name': 'nllb-200-distilled-600M',
            'provider': 'ollama',
            'size': '600M',
            'languages': ['en', 'vi', 'ja', 'ko', 'ru', 'fa', 'zh', 'th', 'id', 'ms', 'de', 'fr', 'es', 'it'],
            'description': 'Meta NLLB-200 distilled model - Best for multilingual translation'
        },
        'nllb-200-large': {
            'name': 'nllb-200-1.3B',
            'provider': 'ollama', 
            'size': '1.3B',
            'languages': ['en', 'vi', 'ja', 'ko', 'ru', 'fa', 'zh', 'th', 'id', 'ms', 'de', 'fr', 'es', 'it'],
            'description': 'Meta NLLB-200 large model - Higher quality, more resource intensive'
        },
        'mt5-base': {
            'name': 'mt5-base',
            'provider': 'huggingface',
            'size': '580M',
            'languages': ['en', 'vi', 'ja', 'ko', 'ru', 'fa', 'zh', 'th', 'id', 'ms'],
            'description': 'Google mT5 base model - Good balance of quality and speed'
        }
    }
    
    # Default model
    DEFAULT_MODEL = os.getenv('DEFAULT_TRANSLATION_MODEL', 'llama2:latest')
    
    # Supported Languages
    SUPPORTED_LANGUAGES = ['en', 'vi', 'ja', 'ko', 'ru', 'fa', 'zh', 'th', 'id', 'ms', 'de', 'fr', 'es', 'it']
    
    LANGUAGE_NAMES = {
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
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    # Cache Configuration
    CACHE_ENABLED = os.getenv('TRANSLATION_CACHE', 'False').lower() == 'true'
    CACHE_TTL = int(os.getenv('TRANSLATION_CACHE_TTL', '86400'))  # 24 hours
    
    # Performance Configuration
    MAX_CONCURRENT_TRANSLATIONS = int(os.getenv('MAX_CONCURRENT_TRANSLATIONS', '3'))
    MAX_TEXT_LENGTH = int(os.getenv('MAX_TEXT_LENGTH', '4000'))  # Max chars per translation
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('TRANSLATION_LOG_FILE', './logs/language_translation.log')
    
    @classmethod
    def get_model_config(cls, model_name: str) -> Dict[str, Any]:
        """Get configuration for specific model"""
        return cls.SUPPORTED_MODELS.get(model_name, cls.SUPPORTED_MODELS[cls.DEFAULT_MODEL])
    
    @classmethod
    def get_supported_languages(cls, model_name: str = None) -> List[str]:
        """Get supported languages for model"""
        if model_name and model_name in cls.SUPPORTED_MODELS:
            return cls.SUPPORTED_MODELS[model_name]['languages']
        return cls.SUPPORTED_LANGUAGES
    
    @classmethod
    def validate_config(cls) -> List[str]:
        """Validate configuration and return any issues"""
        issues = []
        
        if not cls.DATABASE_URL:
            issues.append("DATABASE_URL not configured")
        
        if cls.DEFAULT_MODEL not in cls.SUPPORTED_MODELS:
            issues.append(f"DEFAULT_MODEL '{cls.DEFAULT_MODEL}' not supported")
        
        return issues

# Global config instance
config = TranslationConfig()
