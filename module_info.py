"""
Module information for Language Translation ability
"""
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add parent directory to path for imports
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from lkwolfSAI_ablilities.module_interface import ModuleInfo, ModuleStatus
except ImportError:
    # Fallback if module_interface is not available
    class ModuleStatus:
        EXPERIMENTAL = "experimental"
        ACTIVE = "active"
    
    class ModuleInfo:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

def get_module_info() -> ModuleInfo:
    """Return module metadata"""
    return ModuleInfo(
        name="language_translation",
        version="1.0.0",
        description="Local AI translation service using Ollama",
        author="lkwolfSAI Team",
        status=ModuleStatus.EXPERIMENTAL,
        dependencies=[
            "ollama",
            "asyncio",
            "aiohttp",
            "click",
            "rich",
            "python-dotenv",
            "beautifulsoup4"
        ],
        supported_languages=["en", "vi", "ja", "ko", "ru", "fa", "zh"],
        required_services=["database"],
        config_schema={
            "DATABASE_URL": {
                "type": "string",
                "default": "postgresql://lkwolf:admin!23$%@localhost:5432/lkwolfsai",
                "description": "Database connection URL"
            },
            "OLLAMA_BASE_URL": {
                "type": "string",
                "default": "http://localhost:11434",
                "description": "Ollama server base URL"
            },
            "LOG_LEVEL": {
                "type": "string",
                "default": "INFO",
                "description": "Logging level"
            }
        },
        commands=[
            {
                "name": "translate",
                "description": "Translate text between languages",
                "options": [
                    {
                        "name": "--text",
                        "type": "string",
                        "required": True,
                        "help": "Text to translate"
                    },
                    {
                        "name": "--target",
                        "type": "string",
                        "required": True,
                        "help": "Target language code"
                    },
                    {
                        "name": "--source",
                        "type": "string",
                        "required": False,
                        "help": "Source language code (auto-detect if not specified)"
                    }
                ]
            },
            {
                "name": "interactive",
                "description": "Interactive translation mode",
                "options": []
            }
        ]
    )
