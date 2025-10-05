# 🔌 API Reference - Language Translation

Programmatic API for integrating Language Translation plugin with Ollama AI models.

## 📋 Overview

The Language Translation plugin provides both CLI and programmatic interfaces. This document covers the programmatic API for developers who want to integrate translation functionality using local Ollama models into their applications.

## 🏗️ Architecture

```
Your Application
       ↓
TranslationCLI
       ↓
TranslationService
       ↓
┌─────────────────┬─────────────────┬─────────────────┐
│  AILocalTranslator │ TranslationCache │   Database     │
│  (Ollama Client)  │    Service      │   Manager      │
└─────────────────┴─────────────────┴─────────────────┘
       ↓
Ollama Service (localhost:11434)
```

## 🚀 Quick Start

### Basic Integration

```python
import sys
from pathlib import Path

# Add module to path
sys.path.append(str(Path(__file__).parent / "lkwolfSAI_ablilities" / "language_translation"))

from services.translation_service import TranslationService

# Initialize service
translation_service = TranslationService()

# Translate text using Ollama
async def translate_text():
    result = await translation_service.translate_text(
        text="Hello world",
        target_language="vi",
        source_language="en"
    )
    return result

# Get supported languages
async def get_languages():
    languages = await translation_service.get_supported_languages()
    return languages
```

## 🔧 Core Classes

### TranslationService

Main service class for translation operations.

```python
class TranslationService:
    """Main translation service using AI local models"""
    
    async def translate_text(
        self, 
        text: str, 
        target_language: str, 
        source_language: str = 'auto'
    ) -> Optional[str]:
        """
        Translate text from source to target language
        
        Args:
            text: Text to translate
            target_language: Target language code
            source_language: Source language code (default: auto-detect)
            
        Returns:
            Translated text or None if failed
        """
    
    async def translate_to_all_languages(
        self, 
        text: str, 
        source_language: str = 'auto'
    ) -> Dict[str, str]:
        """
        Translate text to all supported languages
        
        Args:
            text: Text to translate
            source_language: Source language code
            
        Returns:
            Dictionary mapping language codes to translations
        """
    
    async def detect_language(self, text: str) -> str:
        """
        Detect the language of given text
        
        Args:
            text: Text to analyze
            
        Returns:
            Detected language code
        """
    
    async def get_supported_languages(self) -> Dict[str, str]:
        """
        Get supported languages with their names
        
        Returns:
            Dictionary mapping language codes to language names
        """
    
    async def batch_translate(
        self, 
        texts: List[str], 
        target_language: str, 
        source_language: str = 'auto'
    ) -> List[Optional[str]]:
        """
        Translate multiple texts
        
        Args:
            texts: List of texts to translate
            target_language: Target language code
            source_language: Source language code
            
        Returns:
            List of translated texts (None for failed translations)
        """
```

### AILocalTranslator

Core translation engine using Ollama.

```python
class AILocalTranslator:
    """AI-powered local translation using Ollama models"""
    
    async def translate_text(
        self, 
        text: str, 
        target_language: str, 
        source_language: str = 'auto'
    ) -> Optional[str]:
        """Translate text using AI model"""
    
    async def translate_to_all_languages(
        self, 
        text: str, 
        source_language: str = 'auto'
    ) -> Dict[str, str]:
        """Translate to all supported languages"""
    
    async def detect_language(self, text: str) -> str:
        """Detect language of text"""
    
    async def get_model_info(self) -> Dict[str, Any]:
        """Get information about current model"""
```

### TranslationCacheService

Manages translation caching.

```python
class TranslationCacheService:
    """Service for managing translation cache"""
    
    async def get_cached_translation(
        self, 
        source_text: str, 
        source_lang: str, 
        target_lang: str
    ) -> Optional[Dict[str, Any]]:
        """Get cached translation if available"""
    
    async def cache_translation(
        self, 
        source_text: str, 
        source_lang: str, 
        target_lang: str, 
        translated_text: str, 
        model_used: str, 
        confidence_score: float = None
    ):
        """Cache translation result"""
    
    async def clear_cache(
        self, 
        source_lang: str = None, 
        target_lang: str = None
    ):
        """Clear cache entries"""
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
```

## 📊 Data Models

### TranslationRequest (Database Model)

```python
class TranslationRequest(Base):
    """Translation request database model"""
    __tablename__ = 'translation_requests'
    
    id = Column(Integer, primary_key=True)
    source_text = Column(Text, nullable=False)
    source_language = Column(String(10), nullable=False)
    target_language = Column(String(10), nullable=False)
    translated_text = Column(Text, nullable=True)
    model_used = Column(String(50), nullable=False)
    status = Column(String(20), default='pending')
    confidence_score = Column(Float, nullable=True)
    processing_time = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### TranslationCache (Database Model)

```python
class TranslationCache(Base):
    """Translation cache database model"""
    __tablename__ = 'translation_cache'
    
    id = Column(Integer, primary_key=True)
    source_text = Column(Text, nullable=False)
    source_language = Column(String(10), nullable=False)
    target_language = Column(String(10), nullable=False)
    translated_text = Column(Text, nullable=False)
    model_used = Column(String(50), nullable=False)
    confidence_score = Column(Float, nullable=True)
    hit_count = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_accessed = Column(DateTime, default=datetime.utcnow)
```

### ModelInfo (Database Model)

```python
class ModelInfo(Base):
    """AI model information database model"""
    __tablename__ = 'model_info'
    
    id = Column(Integer, primary_key=True)
    model_name = Column(String(100), nullable=False, unique=True)
    provider = Column(String(50), nullable=False)
    size = Column(String(20), nullable=True)
    description = Column(Text, nullable=True)
    supported_languages = Column(JSON, nullable=True)
    is_available = Column(Boolean, default=True)
    last_used = Column(DateTime, nullable=True)
    usage_count = Column(Integer, default=0)
    performance_metrics = Column(JSON, nullable=True)
```

## 🔧 Configuration

### Environment Variables

```python
# Ollama Configuration
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
OLLAMA_TIMEOUT = int(os.getenv('OLLAMA_TIMEOUT', '300'))

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL')

# Cache Configuration
CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'True').lower() == 'true'
CACHE_TTL = int(os.getenv('CACHE_TTL', '86400'))

# Performance Configuration
MAX_CONCURRENT_TRANSLATIONS = int(os.getenv('MAX_CONCURRENT_TRANSLATIONS', '3'))
MAX_TEXT_LENGTH = int(os.getenv('MAX_TEXT_LENGTH', '4000'))

# Default Model
DEFAULT_MODEL = os.getenv('DEFAULT_TRANSLATION_MODEL', 'llama2:latest')
```

### Configuration Class

```python
from utils.config import TranslationConfig

# Access configuration
config = TranslationConfig()

# Get model configuration
model_config = config.get_model_config('llama2:latest')

# Get supported languages for model
languages = config.get_supported_languages('llama2:latest')

# Validate configuration
errors = config.validate_config()
```

## 🎯 Usage Examples

### Basic Translation

```python
import asyncio
from services.translation_service import TranslationService

async def basic_translation():
    service = TranslationService()
    
    # Translate single text
    result = await service.translate_text(
        text="Hello world",
        target_language="vi",
        source_language="en"
    )
    
    print(f"Translation: {result}")

# Run translation
asyncio.run(basic_translation())
```

### Batch Translation

```python
async def batch_translation():
    service = TranslationService()
    
    texts = [
        "Hello world",
        "Good morning",
        "How are you?"
    ]
    
    # Translate multiple texts
    results = await service.batch_translate(
        texts=texts,
        target_language="vi",
        source_language="en"
    )
    
    for original, translated in zip(texts, results):
        print(f"{original} -> {translated}")

asyncio.run(batch_translation())
```

### Multi-Language Translation

```python
async def multi_language_translation():
    service = TranslationService()
    
    # Translate to all supported languages
    all_translations = await service.translate_to_all_languages(
        text="Hello world",
        source_language="en"
    )
    
    for lang_code, translation in all_translations.items():
        print(f"{lang_code}: {translation}")

asyncio.run(multi_language_translation())
```

### Language Detection

```python
async def detect_language():
    service = TranslationService()
    
    # Detect language
    detected_lang = await service.detect_language("Bonjour le monde")
    print(f"Detected language: {detected_lang}")
    
    # Get supported languages
    languages = await service.get_supported_languages()
    print(f"Supported languages: {list(languages.keys())}")

asyncio.run(detect_language())
```

### Custom Model Usage

```python
from core.ai_translator import AILocalTranslator

async def custom_model_translation():
    # Initialize with specific model
    translator = AILocalTranslator(model_name="llama2:latest")
    
    # Translate with custom model
    result = await translator.translate_text(
        text="Hello world",
        target_language="vi",
        source_language="en"
    )
    
    # Get model info
    model_info = await translator.get_model_info()
    print(f"Model: {model_info['name']}")
    print(f"Translation: {result}")

asyncio.run(custom_model_translation())
```

### Caching Integration

```python
from services.translation_cache import TranslationCacheService

async def caching_example():
    cache_service = TranslationCacheService()
    translation_service = TranslationService()
    
    text = "Hello world"
    source_lang = "en"
    target_lang = "vi"
    
    # Check cache first
    cached = await cache_service.get_cached_translation(
        text, source_lang, target_lang
    )
    
    if cached:
        print(f"From cache: {cached['translated_text']}")
    else:
        # Translate and cache
        translated = await translation_service.translate_text(
            text, target_lang, source_lang
        )
        
        # Cache the result
        await cache_service.cache_translation(
            text, source_lang, target_lang, translated, "llama2:latest"
        )
        
        print(f"New translation: {translated}")
    
    # Get cache statistics
    stats = await cache_service.get_cache_stats()
    print(f"Cache hit rate: {stats['hit_rate']}")

asyncio.run(caching_example())
```

## 🔍 Ollama Integration

### Direct Ollama Client Usage

```python
from utils.ollama_client import OllamaClient

async def direct_ollama_usage():
    client = OllamaClient()
    
    # Check if Ollama is available
    is_available = await client.is_available()
    if not is_available:
        print("Ollama service not available")
        return
    
    # List available models
    models = await client.list_models()
    print(f"Available models: {models}")
    
    # Translate using specific model
    result = await client.translate(
        text="Hello world",
        source_lang="en",
        target_lang="vi",
        model_name="llama2:latest"
    )
    
    print(f"Translation: {result}")

asyncio.run(direct_ollama_usage())
```

### Custom Ollama Integration

```python
import httpx

async def custom_ollama_request():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama2:latest",
                "prompt": "Translate to Vietnamese: Hello world",
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9
                }
            },
            timeout=300
        )
        
        if response.status_code == 200:
            result = response.json()
            translation = result.get('response', '').strip()
            print(f"Translation: {translation}")

asyncio.run(custom_ollama_request())
```

## 🛠️ Error Handling

### Exception Handling

```python
import logging
from services.translation_service import TranslationService

async def robust_translation():
    service = TranslationService()
    
    try:
        result = await service.translate_text(
            text="Hello world",
            target_language="vi",
            source_language="en"
        )
        
        if result is None:
            print("Translation failed")
            return None
            
        return result
        
    except ConnectionError as e:
        logging.error(f"Ollama connection error: {e}")
        return None
        
    except TimeoutError as e:
        logging.error(f"Translation timeout: {e}")
        return None
        
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None

asyncio.run(robust_translation())
```

### Validation

```python
from utils.config import TranslationConfig

def validate_translation_request(text, target_lang, source_lang=None):
    """Validate translation request parameters"""
    config = TranslationConfig()
    
    errors = []
    
    # Validate text
    if not text or len(text.strip()) == 0:
        errors.append("Text cannot be empty")
    
    if len(text) > config.MAX_TEXT_LENGTH:
        errors.append(f"Text too long (max {config.MAX_TEXT_LENGTH} characters)")
    
    # Validate languages
    supported_langs = config.get_supported_languages()
    if target_lang not in supported_langs:
        errors.append(f"Unsupported target language: {target_lang}")
    
    if source_lang and source_lang != 'auto' and source_lang not in supported_langs:
        errors.append(f"Unsupported source language: {source_lang}")
    
    return errors

# Usage
errors = validate_translation_request("Hello", "vi", "en")
if errors:
    print(f"Validation errors: {errors}")
```

## 📈 Performance Optimization

### Async Best Practices

```python
import asyncio
from services.translation_service import TranslationService

async def concurrent_translations():
    """Perform multiple translations concurrently"""
    
    service = TranslationService()
    texts = [
        "Hello world",
        "Good morning",
        "How are you?",
        "Thank you very much"
    ]
    
    # Create tasks
    tasks = []
    for text in texts:
        task = service.translate_text(text, "vi", "en")
        tasks.append(task)
    
    # Run concurrently
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Handle results
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Translation {i} failed: {result}")
        else:
            print(f"{texts[i]} -> {result}")

asyncio.run(concurrent_translations())
```

### Resource Management

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def translation_service_context():
    """Context manager for translation service"""
    service = TranslationService()
    try:
        yield service
    finally:
        await service.close()

async def use_service():
    async with translation_service_context() as service:
        result = await service.translate_text("Hello", "vi")
        return result

asyncio.run(use_service())
```

### Batch Processing with Progress

```python
import asyncio
from tqdm.asyncio import tqdm

async def batch_translate_with_progress(texts, target_lang):
    """Batch translate with progress bar"""
    
    service = TranslationService()
    results = []
    
    # Process with progress bar
    for text in tqdm(texts, desc="Translating"):
        result = await service.translate_text(text, target_lang)
        results.append(result)
        
        # Small delay to prevent overwhelming Ollama
        await asyncio.sleep(0.1)
    
    return results

# Usage
texts = ["Hello", "World", "Python", "Translation"]
results = asyncio.run(batch_translate_with_progress(texts, "vi"))
```

## 🧪 Testing

### Unit Testing

```python
import pytest
import asyncio
from services.translation_service import TranslationService

@pytest.mark.asyncio
async def test_translation_service():
    service = TranslationService()
    
    # Test basic translation
    result = await service.translate_text("Hello", "vi", "en")
    assert result is not None
    assert isinstance(result, str)
    
    # Test language detection
    detected = await service.detect_language("Bonjour")
    assert detected in ["fr", "auto"]
    
    # Test supported languages
    languages = await service.get_supported_languages()
    assert "vi" in languages
    assert "en" in languages

# Run tests
pytest.main([__file__])
```

### Integration Testing

```python
async def test_full_translation_workflow():
    """Test complete translation workflow"""
    
    service = TranslationService()
    
    # Test single translation
    result = await service.translate_text("Hello world", "vi", "en")
    assert result is not None
    
    # Test batch translation
    texts = ["Hello", "World"]
    results = await service.batch_translate(texts, "vi", "en")
    assert len(results) == 2
    assert all(r is not None for r in results)
    
    # Test multi-language translation
    all_translations = await service.translate_to_all_languages("Hello", "en")
    assert len(all_translations) > 0
    assert "vi" in all_translations

asyncio.run(test_full_translation_workflow())
```

### Mock Testing

```python
from unittest.mock import AsyncMock, patch

async def test_translation_with_mock():
    """Test translation with mocked Ollama"""
    
    with patch('services.translation_service.OllamaClient') as mock_client:
        # Setup mock
        mock_instance = AsyncMock()
        mock_instance.translate.return_value = "Xin chào"
        mock_client.return_value = mock_instance
        
        # Test translation
        service = TranslationService()
        result = await service.translate_text("Hello", "vi", "en")
        
        assert result == "Xin chào"
        mock_instance.translate.assert_called_once()

asyncio.run(test_translation_with_mock())
```

## 📚 Additional Resources

- **[Setup Guide](SETUP.md)** - Installation and configuration
- **[Usage Guide](USAGE.md)** - Command-line usage
- **[README](README.md)** - Module overview

## 🆘 Support

For API-related issues:
1. Check the error logs in `logs/language_translation.log`
2. Verify Ollama service with `python scripts/setup_ollama.py --check`
3. Test basic functionality with `python scripts/test_translation.py --test-basic`
4. Report issues with detailed error messages and configuration

---

**Ready to integrate? Start with the basic translation example above!** 🚀
