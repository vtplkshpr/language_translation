# 📖 Usage Guide - Language Translation

Complete guide for using the Language Translation tool effectively.

## 🎯 Getting Started

### Interactive Mode (Recommended for Beginners)

The interactive mode provides a guided experience:

```bash
python main.py --interactive
```

**Step-by-step process:**
1. **Welcome screen** - Displays available models and languages
2. **Select translation mode** - Single text or batch translation
3. **Enter text** - Input text to translate
4. **Choose languages** - Select source and target languages
5. **Configure options** - Set model, batch size, etc.
6. **View results** - See translations with confidence scores

### Command Line Mode (For Automation)

Perfect for scripts and automated workflows:

```bash
# Basic translation
python main.py --text "Hello world" --target-lang vi

# With source language detection
python main.py --text "Bonjour le monde" --target-lang en --source-lang auto

# Batch translation
python main.py --batch --text "Hello" --text "World" --target-lang vi

# Using specific model
python main.py --text "Test" --target-lang vi --model nllb-200-large
```

## 🔧 Advanced Configuration

### Environment Variables

Create a `.env` file for custom configuration:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TIMEOUT=300

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/translation_db

# Cache Configuration
CACHE_ENABLED=true
CACHE_TTL=86400  # 24 hours

# Performance Settings
MAX_CONCURRENT_TRANSLATIONS=3
MAX_TEXT_LENGTH=4000

# Default Model
DEFAULT_TRANSLATION_MODEL=nllb-200

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/language_translation.log
```

### Command Line Options

```bash
python main.py [OPTIONS]

Options:
  --text, -t TEXT          Text to translate
  --source-lang, -s TEXT   Source language code (default: auto)
  --target-lang, -l TEXT   Target language code (default: vi)
  --model, -m TEXT         AI model to use
  --batch, -b              Batch translation mode
  --interactive, -i        Interactive mode
  --languages              Show supported languages
  --models                 Show available models
  --stats                  Show translation statistics
  --init-db                Initialize database
  --help                   Show help message
```

## 🌍 Language Support

### Supported Languages

| Code | Language | Code | Language |
|------|----------|------|----------|
| `en` | English | `de` | German |
| `vi` | Vietnamese | `fr` | French |
| `ja` | Japanese | `es` | Spanish |
| `ko` | Korean | `it` | Italian |
| `ru` | Russian | `zh` | Chinese |
| `fa` | Persian | `th` | Thai |
| `id` | Indonesian | `ms` | Malay |

### Language Usage Examples

```bash
# English to Vietnamese
python main.py --text "Hello world" --source-lang en --target-lang vi

# Auto-detect source language
python main.py --text "Bonjour le monde" --target-lang en

# Japanese to English
python main.py --text "こんにちは世界" --source-lang ja --target-lang en

# Multiple target languages (batch)
python main.py --text "Hello" --target-lang vi,ja,ko
```

## 🤖 AI Models

### Available Models

#### NLLB-200 Distilled (Recommended)
```bash
# Download and use
ollama pull nllb-200-distilled-600M
python main.py --text "Test" --model nllb-200
```

**Features:**
- Size: 600MB
- Languages: 14+
- Best for: General translation
- Speed: Fast

#### NLLB-200 Large
```bash
# Download and use
ollama pull nllb-200-1.3B
python main.py --text "Test" --model nllb-200-large
```

**Features:**
- Size: 1.3GB
- Languages: 14+
- Best for: High-quality translation
- Speed: Moderate

#### Llama2 (Alternative)
```bash
# Download and use
ollama pull llama2:latest
python main.py --text "Test" --model llama2
```

**Features:**
- Size: 3.8GB
- Languages: 14+
- Best for: General purpose, creative translation
- Speed: Slower

### Model Selection Guide

**For Speed:** Use `nllb-200` (600MB)
**For Quality:** Use `nllb-200-large` (1.3GB)
**For Creativity:** Use `llama2` (3.8GB)

## 📊 Translation Modes

### Single Text Translation

```bash
# Simple translation
python main.py --text "Hello world" --target-lang vi

# With confidence score
python main.py --text "Hello world" --target-lang vi --verbose

# Using specific model
python main.py --text "Hello world" --target-lang vi --model nllb-200-large
```

### Batch Translation

```bash
# Multiple texts
python main.py --batch --text "Hello" --text "World" --text "Test" --target-lang vi

# From file (if implemented)
python main.py --batch --input-file texts.txt --target-lang vi

# Multiple target languages
python main.py --text "Hello" --target-lang vi,ja,ko
```

### Language Detection

```bash
# Auto-detect source language
python main.py --text "Bonjour le monde" --target-lang en --source-lang auto

# Detect language only
python main.py --text "Bonjour le monde" --detect-only
```

## 💾 Caching System

### Cache Configuration

```env
# Enable/disable caching
CACHE_ENABLED=true

# Cache TTL (seconds)
CACHE_TTL=86400  # 24 hours

# Cache database
DATABASE_URL=postgresql://user:password@localhost:5432/translation_db
```

### Cache Usage

```bash
# First translation (will be cached)
python main.py --text "Hello world" --target-lang vi

# Second translation (will use cache)
python main.py --text "Hello world" --target-lang vi

# Clear cache
python main.py --clear-cache
```

### Cache Statistics

```bash
# View cache statistics
python main.py --stats

# Cache info includes:
# - Total cached translations
# - Cache hit rate
# - Storage usage
# - Most translated languages
```

## 🗄️ Database Management

### Database Setup

```bash
# Initialize database
python main.py --init-db

# Or use script
python scripts/init_database.py
```

### Database Tables

- `translation_requests`: Translation history
- `translation_cache`: Cached translations
- `model_info`: AI model information
- `translation_sessions`: Batch translation sessions

### Database Operations

```bash
# View translation history
python main.py --history

# Export translation data
python main.py --export-history --format csv

# Clean old data
python main.py --cleanup --days 30
```

## 🎯 Best Practices

### Text Preparation

**Good text for translation:**
- Complete sentences
- Proper punctuation
- Clear context
- Reasonable length (under 4000 characters)

**Avoid:**
- Very short phrases without context
- Text with special formatting
- Extremely long paragraphs
- Mixed languages in same text

### Model Selection

**For different use cases:**

```bash
# Technical documentation
python main.py --text "API documentation" --model nllb-200 --target-lang vi

# Creative content
python main.py --text "Poetry" --model llama2 --target-lang vi

# General text
python main.py --text "General text" --model nllb-200 --target-lang vi
```

### Performance Optimization

1. **Use caching** - Enable cache for repeated translations
2. **Batch translations** - Process multiple texts together
3. **Choose appropriate model** - Balance quality vs. speed
4. **Monitor memory usage** - Large models need more RAM
5. **Use GPU acceleration** - Configure Ollama for GPU if available

## 🔍 Advanced Features

### Custom Model Integration

```python
# Example: Using custom Ollama model
import httpx

async def translate_with_custom_model(text, target_lang):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "your-custom-model",
                "prompt": f"Translate to {target_lang}: {text}",
                "stream": False
            }
        )
        return response.json()
```

### Batch Processing Script

```python
import asyncio
from services.translation_service import TranslationService

async def batch_translate_file(input_file, output_file, target_lang):
    service = TranslationService()
    
    with open(input_file, 'r', encoding='utf-8') as f:
        texts = f.readlines()
    
    results = []
    for text in texts:
        translated = await service.translate_text(
            text.strip(), 
            target_lang
        )
        results.append(f"{text.strip()} -> {translated}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(results))

# Usage
asyncio.run(batch_translate_file('input.txt', 'output.txt', 'vi'))
```

### Integration with Other Tools

```python
# Example: Translate CSV file
import pandas as pd
from services.translation_service import TranslationService

async def translate_csv(input_file, output_file, target_lang):
    service = TranslationService()
    df = pd.read_csv(input_file)
    
    # Translate specific column
    for index, row in df.iterrows():
        translated = await service.translate_text(
            row['text_column'], 
            target_lang
        )
        df.at[index, 'translated_column'] = translated
    
    df.to_csv(output_file, index=False)

# Usage
asyncio.run(translate_csv('data.csv', 'translated_data.csv', 'vi'))
```

## 🛠️ Troubleshooting

### Common Issues

**Ollama not running:**
```bash
# Check status
python scripts/setup_ollama.py --check

# Start Ollama
ollama serve

# Check logs
journalctl -u ollama -f
```

**Model not found:**
```bash
# List available models
ollama list

# Pull missing model
ollama pull nllb-200-distilled-600M

# Check model info
python main.py --models
```

**Database connection errors:**
```bash
# Test connection
python scripts/test_translation.py --test-db

# Recreate database
python scripts/recreate_tables.py
```

**Translation quality issues:**
```bash
# Try different model
python main.py --text "Your text" --model nllb-200-large

# Check language codes
python main.py --languages

# Verify text format
# Ensure proper punctuation and context
```

### Performance Issues

**Slow translations:**
- Use smaller model (`nllb-200` instead of `nllb-200-large`)
- Enable GPU acceleration in Ollama
- Reduce text length
- Use caching for repeated translations

**High memory usage:**
- Use smaller model
- Reduce concurrent translations
- Restart Ollama service periodically

**Network timeouts:**
- Increase `OLLAMA_TIMEOUT` in configuration
- Check Ollama service status
- Verify firewall settings

## 📈 Monitoring and Analytics

### Translation Statistics

```bash
# View statistics
python main.py --stats

# Statistics include:
# - Total translations performed
# - Most used languages
# - Model performance metrics
# - Cache hit rates
# - Processing times
```

### Performance Monitoring

```bash
# Monitor Ollama resources
htop | grep ollama

# Check database size
python main.py --db-stats

# View logs
tail -f logs/language_translation.log
```

### Export Data

```bash
# Export translation history
python main.py --export-history --format csv

# Export statistics
python main.py --export-stats --format json

# Backup database
pg_dump translation_db > backup.sql
```

---

**Ready to start translating? Try the interactive mode: `python main.py --interactive`** 🚀
