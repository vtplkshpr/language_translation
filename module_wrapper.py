"""
Module wrapper for Language Translation ability
"""
import sys
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Try to import required modules
config = None
translation_service = None
db_service = None

try:
    from utils.config import config
except ImportError:
    pass

try:
    from services.translation_service import translation_service
except ImportError:
    pass

try:
    from services.database import db_service
except ImportError:
    pass

class ModuleInfo:
    """Module information class"""
    def __init__(self, name: str, version: str, description: str, status: str = "experimental"):
        self.name = name
        self.version = version
        self.description = description
        self.status = status
        self.services = []

class ModuleInterface:
    """Base interface for modules"""
    
    def __init__(self):
        self._module_info = ModuleInfo(
            name="language_translation",
            version="1.0.0",
            description="Local AI translation service using Ollama",
            status="experimental"
        )
    
    @property
    def module_info(self):
        """Return module metadata"""
        return self._module_info
    
    async def initialize(self) -> bool:
        """Initialize the module"""
        try:
            # Try to initialize services if available
            if config:
                print("Language Translation module initialized successfully")
                return True
            else:
                print("Language Translation module: Services not available")
                return False
        except Exception as e:
            print(f"Language Translation module initialization failed: {e}")
            return False
    
    async def cleanup(self) -> bool:
        """Cleanup module resources"""
        try:
            print("Language Translation module cleaned up")
            return True
        except Exception as e:
            print(f"Language Translation module cleanup failed: {e}")
            return False
    
    def get_cli_commands(self) -> List[Any]:
        """Get CLI commands for this module"""
        try:
            # Import CLI commands if available
            from main import main
            return [main]
        except ImportError:
            return []
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check"""
        try:
            if config and translation_service:
                return {
                    "status": "healthy",
                    "services": ["translation_service", "database"],
                    "config_loaded": config is not None,
                    "translation_available": translation_service is not None
                }
            else:
                return {
                    "status": "degraded",
                    "services": [],
                    "config_loaded": config is not None,
                    "translation_available": translation_service is not None,
                    "error": "Some services not available"
                }
        except Exception as e:
            return {
                "status": "error",
                "services": [],
                "error": str(e)
            }
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        """Validate module configuration"""
        errors = []
        
        # Check required configuration
        required_keys = []
        
        for key in required_keys:
            if key not in config:
                errors.append(f"Missing required configuration: {key}")
        
        return errors

def get_module_class():
    """Get the module class for registration"""
    return LanguageTranslationModule

class LanguageTranslationModule(ModuleInterface):
    """Language Translation module implementation"""
    
    def __init__(self):
        super().__init__()
        self._module_info.services = ["translation_service", "database"]
    
    async def initialize(self) -> bool:
        """Initialize the translation module"""
        try:
            if config and translation_service:
                print("Language Translation module initialized successfully")
                return True
            else:
                print("Language Translation module: Some services not available")
                return True  # Still return True as it's partially functional
        except Exception as e:
            print(f"Language Translation module initialization failed: {e}")
            return False
