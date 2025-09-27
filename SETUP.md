# 🌍 Language Translation - Setup Guide

**Detailed installation and configuration guide**

## 📋 Overview

Language Translation is a powerful AI-powered multilingual translation tool using local Ollama models. It provides fast, private, and accurate translations without requiring internet connectivity or external API services.

## 🚀 Quick Installation

### Step 1: Install Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Verify Ollama is running
curl http://localhost:11434/api/tags
```

### Step 2: Setup Python Environment

```bash
# Navigate to project directory
cd language-translation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Download AI Models

```bash
# Download NLLB-200 model (approximately 600MB)
python scripts/setup_ollama.py --model nllb-200

# Or download larger model for better quality (~1.3GB)
python scripts/setup_ollama.py --model nllb-200-large
```

### Step 4: Configure Environment

```bash
# Copy configuration template
cp .env.example .env

# Edit configuration if needed
nano .env
```

### Step 5: Initialize Database (Optional)

```bash
# Initialize database tables for caching
python main.py --init-db
```

### Step 6: Test System

```bash
# Run basic test
python scripts/test_translation.py --init-db --test-basic

# Run full test
python scripts/test_translation.py --init-db
```

## 🎮 Usage

### Interactive Mode (Recommended)

```bash
python main.py --interactive
```

### Single Translation

```bash
# Translate from English to Vietnamese
python main.py --text "Hello world" --target-lang vi

# Translate with auto-detect source language
python main.py --text "Xin chào" --target-lang en --source-lang auto
```

### Batch Translation

```bash
# Translate multiple texts at once
python main.py --batch --text "Hello\nGood morning\nThank you" --target-lang vi
```

### View Information

```bash
# View supported languages
python main.py --languages

# View available models
python main.py --models

# View statistics
python main.py --stats
```

## 🔧 Advanced Configuration

### Supported Models

| Model | Size | Quality | Speed | Description |
|-------|------|---------|-------|-------------|
| nllb-200 | 600MB | Good | Fast | Default model, balanced |
| nllb-200-large | 1.3GB | Excellent | Slower | Highest quality |
| mt5-base | 580MB | Good | Fast | Google mT5 model |

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

### Performance Configuration

```env
# In .env file
MAX_CONCURRENT_TRANSLATIONS=3    # Number of concurrent translations
MAX_TEXT_LENGTH=4000            # Maximum text length
TRANSLATION_CACHE_TTL=86400     # Cache time (seconds)
```

## 🛠️ Troubleshooting

### Ollama Service Issues

```bash
# Check Ollama service status
sudo systemctl status ollama

# Restart Ollama service
sudo systemctl restart ollama

# Or start manually
ollama serve
```

### Model Not Found Errors

```bash
# Check installed models
ollama list

# Reinstall model
ollama pull nllb-200-distilled-600M
```

### Database Connection Issues

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test database connection
python scripts/test_translation.py --init-db
```

### Memory/Performance Issues

```bash
# Reduce concurrent translations
# In .env: MAX_CONCURRENT_TRANSLATIONS=1

# Or use smaller model
python scripts/setup_ollama.py --model nllb-200
```

## 📊 Monitoring and Logs

### View Logs

```bash
# Translation service logs
tail -f logs/language_translation.log

# Ollama logs
journalctl -u ollama -f
```

### View Statistics

```bash
python main.py --stats
```

## 🔄 Updates and Maintenance

### Update Models

```bash
# Update to latest model
ollama pull nllb-200-distilled-600M

# Or use setup script
python scripts/setup_ollama.py --model nllb-200
```

### Cache Cleanup

```bash
# Old cache is automatically cleaned after TTL
# Or clean manually via API
```

### Backup and Restore

```bash
# Backup models
ollama list > models_backup.txt

# Restore models
while read model; do ollama pull $model; done < models_backup.txt
```

## 📚 Additional Resources

- **[Usage Guide](USAGE.md)**: Complete usage instructions
- **[API Reference](API.md)**: Programmatic API documentation
- **[README](README.md)**: Module overview and quick start

## 🎉 Conclusion

Language Translation provides:

- ✅ **Local Translation**: No internet required, high security
- ✅ **AI Quality**: Uses Meta's NLLB-200 models
- ✅ **Multi-language**: Supports 14+ languages
- ✅ **Smart Caching**: Speeds up repeated translations
- ✅ **Friendly CLI**: Easy-to-use interface
- ✅ **Fast Processing**: Local inference for quick results

The system is ready to use after completing the setup steps above!

---

**Language Translation Setup Guide - Ready to start translating!** 🚀
