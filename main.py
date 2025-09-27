"""
Main CLI interface for Language Translation Ability
"""
import asyncio
import click
import logging
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from services.translation_service import translation_service
from utils.config import config
from services.database import db_service

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

console = Console()

class TranslationCLI:
    """CLI interface for language translation"""
    
    def __init__(self):
        self.service = translation_service
    
    def display_banner(self):
        """Display welcome banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                    🌐 LANGUAGE TRANSLATION                   ║
║                                                              ║
║              AI-Powered Local Translation Service            ║
║                   Using Ollama + NLLB-200                   ║
╚══════════════════════════════════════════════════════════════╝
        """
        console.print(Panel(banner, style="bold blue"))
    
    def display_supported_languages(self):
        """Display supported languages"""
        languages = config.LANGUAGE_NAMES
        
        table = Table(title="Supported Languages")
        table.add_column("Code", style="cyan")
        table.add_column("Language", style="green")
        table.add_column("Code", style="cyan")
        table.add_column("Language", style="green")
        
        # Add languages in pairs
        lang_items = list(languages.items())
        for i in range(0, len(lang_items), 2):
            row = []
            row.extend(lang_items[i])
            if i + 1 < len(lang_items):
                row.extend(lang_items[i + 1])
            else:
                row.extend(["", ""])
            table.add_row(*row)
        
        console.print(table)
    
    def display_models(self):
        """Display available AI models"""
        models = config.SUPPORTED_MODELS
        
        table = Table(title="Available AI Models")
        table.add_column("Model", style="cyan")
        table.add_column("Size", style="green")
        table.add_column("Provider", style="yellow")
        table.add_column("Description", style="white")
        
        for model_name, model_info in models.items():
            table.add_row(
                model_name,
                model_info['size'],
                model_info['provider'],
                model_info['description']
            )
        
        console.print(table)
    
    async def translate_interactive(self):
        """Interactive translation mode"""
        console.print("\n[bold green]🔄 Interactive Translation Mode[/bold green]")
        
        # Initialize service
        if not await self.service.initialize():
            console.print("[bold red]❌ Failed to initialize translation service[/bold red]")
            return
        
        # Get model info
        model_info = await self.service.get_model_info()
        console.print(f"[cyan]Using model: {model_info.get('name', 'Unknown')}[/cyan]")
        
        while True:
            try:
                console.print("\n" + "="*60)
                
                # Get source text
                source_text = click.prompt("Enter text to translate", type=str)
                if source_text.lower() in ['quit', 'exit', 'q']:
                    break
                
                # Get source language
                source_lang = click.prompt(
                    "Source language (or 'auto' for detection)", 
                    default='auto',
                    type=str
                )
                
                # Get target language
                target_lang = click.prompt(
                    "Target language", 
                    default='vi',
                    type=str
                )
                
                # Translate
                console.print(f"\n[bold yellow]Translating: {source_text[:50]}...[/bold yellow]")
                
                translated = await self.service.translate_text(
                    source_text, target_lang, source_lang
                )
                
                if translated:
                    console.print(f"[bold green]✅ Translation:[/bold green]")
                    console.print(Panel(translated, title="Result", style="green"))
                else:
                    console.print("[bold red]❌ Translation failed[/bold red]")
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Translation interrupted[/yellow]")
                break
            except Exception as e:
                console.print(f"[bold red]Error: {e}[/bold red]")
    
    async def translate_batch(self, texts: list, source_lang: str, target_lang: str):
        """Batch translation mode"""
        console.print(f"\n[bold green]🔄 Batch Translation Mode[/bold green]")
        console.print(f"Translating {len(texts)} texts from {source_lang} to {target_lang}")
        
        # Initialize service
        if not await self.service.initialize():
            console.print("[bold red]❌ Failed to initialize translation service[/bold red]")
            return
        
        results = []
        with console.status("[bold green]Translating..."):
            results = await self.service.batch_translate(texts, target_lang, source_lang)
        
        # Display results
        table = Table(title="Batch Translation Results")
        table.add_column("Original", style="cyan")
        table.add_column("Translation", style="green")
        table.add_column("Status", style="yellow")
        
        for i, (original, translated) in enumerate(zip(texts, results)):
            status = "✅ Success" if translated else "❌ Failed"
            table.add_row(
                original[:50] + "..." if len(original) > 50 else original,
                translated[:50] + "..." if translated and len(translated) > 50 else (translated or ""),
                status
            )
        
        console.print(table)
    
    async def show_stats(self):
        """Show translation statistics"""
        console.print("\n[bold green]📊 Translation Statistics[/bold green]")
        
        # Get cache stats
        from services.translation_cache import TranslationCacheService
        cache_service = TranslationCacheService()
        cache_stats = await cache_service.get_cache_stats()
        
        stats_table = Table(title="Cache Statistics")
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green")
        
        stats_table.add_row("Database Cache Entries", str(cache_stats['database_entries']))
        stats_table.add_row("Memory Cache Entries", str(cache_stats['memory_entries']))
        stats_table.add_row("Total Cache Hits", str(cache_stats['total_hits']))
        stats_table.add_row("Cache TTL (seconds)", str(cache_stats['cache_ttl']))
        
        console.print(stats_table)

@click.command()
@click.option('--text', '-t', help='Text to translate')
@click.option('--source-lang', '-s', default='auto', help='Source language code')
@click.option('--target-lang', '-l', default='vi', help='Target language code')
@click.option('--model', '-m', default=None, help='AI model to use')
@click.option('--batch', '-b', is_flag=True, help='Batch translation mode')
@click.option('--interactive', '-i', is_flag=True, help='Interactive mode')
@click.option('--languages', is_flag=True, help='Show supported languages')
@click.option('--models', is_flag=True, help='Show available models')
@click.option('--stats', is_flag=True, help='Show translation statistics')
@click.option('--init-db', is_flag=True, help='Initialize database')
def main(text, source_lang, target_lang, model, batch, interactive, languages, models, stats, init_db):
    """Language Translation CLI - AI-powered local translation service"""
    
    cli = TranslationCLI()
    
    async def run_async():
        # Initialize database if requested
        if init_db:
            console.print("[bold yellow]Initializing database...[/bold yellow]")
            await db_service.create_tables()
            console.print("[bold green]✅ Database initialized[/bold green]")
            return
        
        # Show supported languages
        if languages:
            cli.display_banner()
            cli.display_supported_languages()
            return
        
        # Show available models
        if models:
            cli.display_banner()
            cli.display_models()
            return
        
        # Show statistics
        if stats:
            cli.display_banner()
            await cli.show_stats()
            return
        
        # Interactive mode
        if interactive:
            cli.display_banner()
            cli.display_supported_languages()
            await cli.translate_interactive()
            return
        
        # Batch mode
        if batch:
            cli.display_banner()
            if not text:
                console.print("[bold red]❌ Please provide text for batch translation[/bold red]")
                return
            
            texts = [line.strip() for line in text.split('\n') if line.strip()]
            await cli.translate_batch(texts, source_lang, target_lang)
            return
        
        # Single translation
        if text:
            cli.display_banner()
            
            # Initialize service
            if not await cli.service.initialize():
                console.print("[bold red]❌ Failed to initialize translation service[/bold red]")
                return
            
            console.print(f"[bold yellow]Translating: {text[:50]}...[/bold yellow]")
            
            translated = await cli.service.translate_text(text, target_lang, source_lang)
            
            if translated:
                console.print(f"[bold green]✅ Translation:[/bold green]")
                console.print(Panel(translated, title="Result", style="green"))
            else:
                console.print("[bold red]❌ Translation failed[/bold red]")
        else:
            # Default: show banner and help
            cli.display_banner()
            console.print("\n[bold cyan]Usage Examples:[/bold cyan]")
            console.print("  [green]python main.py --interactive[/green]          # Interactive mode")
            console.print("  [green]python main.py --text 'Hello' --target-lang vi[/green]  # Single translation")
            console.print("  [green]python main.py --languages[/green]            # Show supported languages")
            console.print("  [green]python main.py --models[/green]               # Show available models")
            console.print("  [green]python main.py --stats[/green]                # Show statistics")
    
    # Run async function
    asyncio.run(run_async())

if __name__ == "__main__":
    main()
