# 🌍 Language Translation

**AI-powered multilingual translation tool using local Ollama models**

## 🎯 Overview

Language Translation is a powerful tool for translating text between multiple languages using local AI models. It provides fast, private, and accurate translations without requiring internet connectivity or external API services.

## ✨ Features

- **🤖 Local AI Translation**: Uses Ollama with NLLB-200 models
- **🌍 Multi-language Support**: 14+ languages supported
- **⚡ Fast Processing**: Local inference for quick results
- **🔒 Privacy-Focused**: No data sent to external services
- **📊 Translation Cache**: Intelligent caching for repeated translations
- **🎨 Beautiful CLI**: Rich terminal interface
- **📈 Batch Processing**: Translate multiple texts efficiently
- **🗄️ Database Storage**: PostgreSQL for translation history and cache

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Ollama installed and running
- PostgreSQL database (optional, for caching)

### Installation

1. **Clone or download this module**
```bash
# If standalone installation
git clone <your-repo-url> language-translation
cd language-translation
```

2. **Install Ollama**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve
```

3. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Download AI models**
```bash
# Download NLLB-200 model (600MB)
python scripts/setup_ollama.py --model nllb-200

# Or download larger model for better quality (1.3GB)
python scripts/setup_ollama.py --model nllb-200-large
```

6. **Setup database (optional)**
```bash
# Initialize database for caching
python main.py --init-db
```

### Usage

#### Interactive Mode (Recommended)
```bash
python main.py --interactive
```

#### Command Line Mode
```bash
# Basic translation
python main.py --text "Hello world" --target-lang vi

# Batch translation
python main.py --batch --text "Hello" --text "World" --target-lang vi

# Language detection
python main.py --text "Bonjour le monde" --target-lang en --source-lang auto
```

## 📖 Detailed Documentation

- **[Setup Guide](SETUP.md)** - Detailed installation and configuration
- **[Usage Guide](USAGE.md)** - Complete usage instructions
- **[API Reference](API.md)** - Programmatic API documentation

## 🏗️ Architecture

```
language_translation/
├── main.py                    # CLI entry point
├── core/                      # Core translation logic
│   └── ai_translator.py      # AI translation service
├── services/                  # Business services
│   ├── translation_service.py # Main translation orchestration
│   ├── translation_cache.py   # Translation caching
│   └── database.py           # Database management
├── models/                    # Database models
│   └── translation_models.py # SQLAlchemy models
├── utils/                     # Utilities
│   ├── config.py             # Configuration management
│   └── ollama_client.py      # Ollama API client
└── scripts/                   # Helper scripts
    ├── setup_ollama.py       # Ollama setup
    ├── init_database.py      # Database initialization
    └── test_translation.py   # Testing scripts
```

## 🌍 Supported Languages

| Code | Language | Code | Language |
|------|----------|------|----------|
| `en` | English | `de` | German |
| `vi` | Vietnamese | `fr` | French |
| `ja` | Japanese | `es` | Spanish |
| `ko` | Korean | `it` | Italian |
| `ru` | Russian | `zh` | Chinese |
| `fa` | Persian | `th` | Thai |
| `id` | Indonesian | `ms` | Malay |

## 🔧 Configuration

### Environment Variables

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TIMEOUT=300

# Database Configuration (Optional)
DATABASE_URL=postgresql://user:password@localhost:5432/translation_db

# Cache Configuration
CACHE_ENABLED=true
CACHE_TTL=86400  # 24 hours

# Performance Configuration
MAX_CONCURRENT_TRANSLATIONS=3
MAX_TEXT_LENGTH=4000

# Default Model
DEFAULT_TRANSLATION_MODEL=nllb-200

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/language_translation.log
```

### Model Configuration

```python
# Available models
SUPPORTED_MODELS = {
    'llama2': {
        'name': 'llama2:latest',
        'size': '3.8GB',
        'languages': ['en', 'vi', 'ja', 'ko', 'ru', 'fa', 'zh', 'th', 'id', 'ms', 'de', 'fr', 'es', 'it'],
        'description': 'High quality general purpose model'
    },
    'nllb-200': {
        'name': 'nllb-200-distilled-600M',
        'size': '600M',
        'languages': ['en', 'vi', 'ja', 'ko', 'ru', 'fa', 'zh', 'th', 'id', 'ms', 'de', 'fr', 'es', 'it'],
        'description': 'Best for multilingual translation'
    },
    'nllb-200-large': {
        'name': 'nllb-200-1.3B',
        'size': '1.3B',
        'languages': ['en', 'vi', 'ja', 'ko', 'ru', 'fa', 'zh', 'th', 'id', 'ms', 'de', 'fr', 'es', 'it'],
        'description': 'Higher quality, more resource intensive'
    }
}
```

## 📊 Output Examples

### Translation Results

```json
{
    "source_text": "Hello world",
    "translated_text": "Xin chào thế giới",
    "source_language": "en",
    "target_language": "vi",
    "model_used": "nllb-200-distilled-600M",
    "confidence_score": 0.95,
    "processing_time": 1.2
}
```

### Batch Translation

```json
[
    {
        "source_text": "Hello",
        "translated_text": "Xin chào",
        "source_language": "en",
        "target_language": "vi"
    },
    {
        "source_text": "World",
        "translated_text": "Thế giới",
        "source_language": "en",
        "target_language": "vi"
    }
]
```

## 🛠️ Troubleshooting

### Ollama Issues

```bash
# Check Ollama status
python scripts/setup_ollama.py --check

# List installed models
python scripts/setup_ollama.py --list

# Restart Ollama service
sudo systemctl restart ollama
```

### Database Issues

```bash
# Test database connection
python scripts/test_translation.py --test-db

# Recreate database tables
python scripts/recreate_tables.py
```

### Model Issues

```bash
# Check available models
ollama list

# Pull missing model
ollama pull nllb-200-distilled-600M

# Test model functionality
python scripts/test_translation.py --test-basic
```

## 🧪 Testing

```bash
# Test basic functionality
python scripts/test_translation.py --test-basic

# Test batch translation
python scripts/test_translation.py --test-batch

# Test caching
python scripts/test_translation.py --test-cache

# Full test suite
python -m pytest tests/
```

## 📈 Performance Tips

1. **Use appropriate model size** - Balance quality vs. speed
2. **Enable caching** - For repeated translations
3. **Batch translations** - Process multiple texts together
4. **Monitor memory usage** - Large models require more RAM
5. **Use GPU acceleration** - If available, configure Ollama for GPU

## 🔒 Privacy & Security

- **Local Processing**: All translations happen locally
- **No External APIs**: No data sent to external services
- **Configurable Storage**: Choose what to store in database
- **Secure Configuration**: Environment variables for sensitive data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Issues**: Report bugs and feature requests on GitHub Issues
- **Documentation**: Check the documentation files in this repository
- **Community**: Join our community discussions

---

**Ready to start translating? Run `python main.py --interactive` and begin!** 🚀
