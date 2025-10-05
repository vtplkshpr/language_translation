"""
Language Translation Plugin for lkwolfSAI Ecosystem
Plug-and-Play Implementation
"""
import asyncio
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Add current directory to path for imports if not already present
current_dir = str(Path(__file__).parent)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import BasePlugin
sys.path.append(str(Path(__file__).parent.parent))
from base_plugin import BasePlugin, PluginInfo, PluginStatus

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class LanguageTranslationPlugin(BasePlugin):
    """Language Translation plugin implementation"""
    
    def __init__(self):
        self._plugin_info = PluginInfo(
            name="language_translation",
            version="1.0.0",
            description="AI-powered translation using local Ollama models",
            author="lkwolfSAI Team",
            status=PluginStatus.ACTIVE,
            dependencies=[
                "click>=8.0.0",
                "rich>=13.0.0",
                "requests>=2.25.0"
            ],
            supported_languages=["en", "vi", "ja", "ko", "ru", "fa", "zh"],
            required_services=[],
            config_schema={
                "OLLAMA_BASE_URL": {
                    "type": "string",
                    "default": "http://localhost:11434",
                    "description": "Ollama API base URL"
                },
                "DEFAULT_MODEL": {
                    "type": "string",
                    "default": "llama2",
                    "description": "Default translation model"
                }
            },
            commands=[
                {
                    "name": "translate",
                    "description": "Translate text between languages",
                    "options": [
                        {
                            "name": "text",
                            "type": "string",
                            "required": True,
                            "help": "Text to translate"
                        },
                        {
                            "name": "target-lang",
                            "type": "string",
                            "required": True,
                            "help": "Target language code"
                        },
                        {
                            "name": "source-lang",
                            "type": "string",
                            "required": False,
                            "help": "Source language code (auto-detect if not provided)"
                        }
                    ]
                }
            ]
        )
        self._initialized = False
    
    @property
    def plugin_info(self) -> PluginInfo:
        """Return plugin metadata"""
        return self._plugin_info
    
    async def initialize(self) -> bool:
        """Initialize plugin"""
        try:
            logger.info(f"Initializing {self.plugin_info.name}...")
            
            # Check if Ollama is available (optional)
            try:
                import requests
                ollama_url = "http://localhost:11434"
                response = requests.get(f"{ollama_url}/api/tags", timeout=5)
                if response.status_code == 200:
                    logger.info("✓ Ollama service is available")
                else:
                    logger.warning("Ollama service not responding properly")
            except Exception as e:
                logger.warning(f"Ollama service check failed: {e}")
                logger.info("Plugin will work in limited mode without Ollama")
            
            self._initialized = True
            logger.info(f"✓ {self.plugin_info.name} initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize {self.plugin_info.name}: {e}")
            return False
    
    async def cleanup(self) -> bool:
        """Cleanup plugin resources"""
        try:
            logger.info(f"Cleaning up {self.plugin_info.name}...")
            self._initialized = False
            logger.info(f"✓ {self.plugin_info.name} cleaned up successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to cleanup {self.plugin_info.name}: {e}")
            return False
    
    def get_cli_commands(self) -> list:
        """Return Click commands for CLI integration"""
        return [main]
    
    async def health_check(self) -> Dict[str, Any]:
        """Return plugin health status"""
        health_status = {
            "plugin": self.plugin_info.name,
            "version": self.plugin_info.version,
            "status": "healthy" if self._initialized else "not_initialized",
            "services": {}
        }
        
        try:
            # Check Ollama service (optional)
            try:
                import requests
                response = requests.get("http://localhost:11434/api/tags", timeout=5)
                health_status["services"]["ollama"] = "healthy" if response.status_code == 200 else "unavailable"
            except Exception:
                health_status["services"]["ollama"] = "unavailable"
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            health_status["services"]["error"] = str(e)
        
        return health_status
    
    def validate_config(self, config: Dict[str, Any]) -> list:
        """Validate plugin configuration"""
        errors = []
        
        # Validate Ollama URL
        if "OLLAMA_BASE_URL" in config:
            url = config["OLLAMA_BASE_URL"]
            if not url or not url.startswith("http"):
                errors.append("OLLAMA_BASE_URL must be a valid HTTP URL")
        
        return errors
    
    async def run(self, data: Any = None) -> Any:
        """Main plugin execution method"""
        if not self._initialized:
            await self.initialize()
        
        return {
            "status": "success",
            "message": f"{self.plugin_info.name} executed",
            "data": data
        }
    
    async def translate_text(self, text: str, target_lang: str, source_lang: str = None) -> str:
        """Translate text using Ollama or fallback method"""
        try:
            import requests
            
            # Try Ollama first
            try:
                # Prepare translation prompt
                if source_lang:
                    prompt = f"Translate this text from {source_lang} to {target_lang}. Return only the Vietnamese translation:\n\n{text}\n\nTranslation:"
                else:
                    prompt = f"Translate this text to Vietnamese ({target_lang}). Return only the Vietnamese translation:\n\n{text}\n\nTranslation:"
                
                # Call Ollama API
                ollama_url = "http://localhost:11434"
                payload = {
                    "model": "llama2:latest",
                    "prompt": prompt,
                    "stream": False
                }
                
                response = requests.post(f"{ollama_url}/api/generate", json=payload, timeout=120)
                
                if response.status_code == 200:
                    result = response.json()
                    translation = result.get("response", "Translation failed")
                    # Clean up the response to get only the translation
                    if "Translation:" in translation:
                        translation = translation.split("Translation:")[-1].strip()
                    return translation
                else:
                    raise Exception(f"Ollama API error: HTTP {response.status_code}")
                    
            except Exception as ollama_error:
                logger.warning(f"Ollama translation failed: {ollama_error}")
                # Fallback to simple translation
                return self._fallback_translation(text, target_lang, source_lang)
                
        except Exception as e:
            return f"Translation error: {str(e)}"
    
    def _fallback_translation(self, text: str, target_lang: str, source_lang: str = None) -> str:
        """Fallback translation method"""
        # Simple language mapping for demonstration
        lang_names = {
            "en": "English",
            "vi": "Vietnamese", 
            "ja": "Japanese",
            "ko": "Korean",
            "ru": "Russian",
            "fa": "Persian",
            "zh": "Chinese"
        }
        
        target_name = lang_names.get(target_lang, target_lang)
        source_name = lang_names.get(source_lang, source_lang) if source_lang else "auto-detected"
        
        return f"[Fallback] Translation from {source_name} to {target_name}: {text} (Note: Ollama service not available)"

# CLI Implementation
console = Console()

class LanguageTranslationCLI:
    """CLI interface for language translation"""
    
    def __init__(self):
        self.plugin = LanguageTranslationPlugin()
    
    async def run_translation(self, text: str = None, target_lang: str = None, 
                            source_lang: str = None, languages: bool = False,
                            interactive: bool = False):
        """Run translation"""
        
        if not await self.plugin.initialize():
            console.print("[red]Failed to initialize plugin[/red]")
            return
        
        try:
            if languages:
                await self._show_supported_languages()
                return
            
            if interactive:
                await self._interactive_mode()
                return
            
            if not text or not target_lang:
                console.print("[red]Error: Please provide text and target language[/red]")
                console.print("Use --help for more information")
                return
            
            # Run translation
            await self._run_translation(text, target_lang, source_lang)
            
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
        finally:
            await self.plugin.cleanup()
    
    async def _run_translation(self, text: str, target_lang: str, source_lang: str):
        """Execute translation"""
        console.print(f"\n[bold blue]🌐 Translating text...[/bold blue]")
        console.print(f"Text: [cyan]{text}[/cyan]")
        console.print(f"Target language: [cyan]{target_lang}[/cyan]")
        if source_lang:
            console.print(f"Source language: [cyan]{source_lang}[/cyan]")
        
        # Translate
        result = await self.plugin.translate_text(text, target_lang, source_lang)
        
        console.print(f"\n[green]✓ Translation result:[/green]")
        console.print(f"[bold]{result}[/bold]")
    
    async def _show_supported_languages(self):
        """Show supported languages"""
        console.print("\n[bold blue]🌍 Supported Languages[/bold blue]")
        
        languages = {
            "en": "English",
            "vi": "Vietnamese",
            "ja": "Japanese",
            "ko": "Korean",
            "ru": "Russian",
            "fa": "Persian",
            "zh": "Chinese (Simplified)"
        }
        
        table = Table(title="Supported Languages")
        table.add_column("Code", style="cyan")
        table.add_column("Language", style="green")
        
        for code, name in languages.items():
            table.add_row(code, name)
        
        console.print(table)
    
    async def _interactive_mode(self):
        """Interactive mode"""
        console.print("\n[bold blue]🎯 Interactive Translation Mode[/bold blue]")
        console.print("[yellow]Interactive mode not implemented yet[/yellow]")

# CLI Commands
@click.command()
@click.option('--text', '-t', help='Text to translate')
@click.option('--target-lang', help='Target language code')
@click.option('--source-lang', help='Source language code (auto-detect if not provided)')
@click.option('--languages', is_flag=True, help='Show supported languages')
@click.option('--interactive', '-i', is_flag=True, help='Interactive mode')
def main(text, target_lang, source_lang, languages, interactive):
    """Language Translation Plugin - AI-powered translation using Ollama"""
    
    if not any([text, target_lang, languages, interactive]):
        console.print("[red]Error: Please provide text and target language, or use --languages or --interactive[/red]")
        console.print("Use --help for more information")
        return
            
    cli = LanguageTranslationCLI()
    asyncio.run(cli.run_translation(
        text=text,
        target_lang=target_lang,
        source_lang=source_lang,
        languages=languages,
        interactive=interactive
    ))

if __name__ == "__main__":
    main()