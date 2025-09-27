"""
Test script for translation service
"""
import asyncio
import click
import logging
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from services.translation_service import translation_service
from services.database import db_service

console = Console()
logging.basicConfig(level=logging.INFO)

@click.command()
@click.option('--init-db', is_flag=True, help='Initialize database')
@click.option('--test-basic', is_flag=True, help='Run basic functionality tests')
@click.option('--test-batch', is_flag=True, help='Run batch translation tests')
@click.option('--test-cache', is_flag=True, help='Run cache tests')
def test_translation(init_db, test_basic, test_batch, test_cache):
    """Test translation service functionality"""
    
    async def run_async():
        console.print(Panel("🧪 Translation Service Tests", style="bold blue"))
        
        # Initialize database
        if init_db:
            console.print("\n[bold yellow]Initializing database...[/bold yellow]")
            await db_service.create_tables()
            console.print("[bold green]✅ Database initialized[/bold green]")
        
        # Test basic functionality
        if test_basic:
            console.print("\n[bold yellow]Testing basic translation...[/bold yellow]")
            
            # Initialize service
            if not await translation_service.initialize():
                console.print("[bold red]❌ Failed to initialize translation service[/bold red]")
                return
            
            # Test single translation
            test_text = "Hello, how are you?"
            translated = await translation_service.translate_text(test_text, 'vi', 'en')
            
            if translated:
                console.print(f"[bold green]✅ Translation test passed[/bold green]")
                console.print(f"[cyan]Original:[/cyan] {test_text}")
                console.print(f"[cyan]Translated:[/cyan] {translated}")
            else:
                console.print("[bold red]❌ Translation test failed[/bold red]")
        
        # Test batch translation
        if test_batch:
            console.print("\n[bold yellow]Testing batch translation...[/bold yellow]")
            
            test_texts = [
                "Hello world",
                "Good morning",
                "How are you?",
                "Thank you very much"
            ]
            
            results = await translation_service.batch_translate(test_texts, 'vi', 'en')
            
            table = Table(title="Batch Translation Results")
            table.add_column("Original", style="cyan")
            table.add_column("Translation", style="green")
            table.add_column("Status", style="yellow")
            
            for original, translated in zip(test_texts, results):
                status = "✅ Success" if translated else "❌ Failed"
                table.add_row(original, translated or "", status)
            
            console.print(table)
        
        # Test cache
        if test_cache:
            console.print("\n[bold yellow]Testing translation cache...[/bold yellow]")
            
            from services.translation_cache import TranslationCacheService
            cache_service = TranslationCacheService()
            
            test_text = "Cache test"
            source_lang = 'en'
            target_lang = 'vi'
            
            # First translation (should cache)
            translated1 = await translation_service.translate_text(test_text, target_lang, source_lang)
            
            # Second translation (should use cache)
            translated2 = await translation_service.translate_text(test_text, target_lang, source_lang)
            
            if translated1 and translated2 and translated1 == translated2:
                console.print("[bold green]✅ Cache test passed[/bold green]")
            else:
                console.print("[bold red]❌ Cache test failed[/bold red]")
            
            # Show cache stats
            stats = await cache_service.get_cache_stats()
            console.print(f"[cyan]Cache entries: {stats['database_entries']}[/cyan]")
            console.print(f"[cyan]Memory cache: {stats['memory_entries']}[/cyan]")
        
        # Run all tests if no specific test selected
        if not any([init_db, test_basic, test_batch, test_cache]):
            console.print("\n[bold yellow]Running all tests...[/bold yellow]")
            
            # Initialize database
            await db_service.create_tables()
            console.print("[bold green]✅ Database initialized[/bold green]")
            
            # Test service initialization
            if await translation_service.initialize():
                console.print("[bold green]✅ Service initialization passed[/bold green]")
                
                # Test single translation
                test_text = "Hello, world!"
                translated = await translation_service.translate_text(test_text, 'vi', 'en')
                if translated:
                    console.print("[bold green]✅ Single translation passed[/bold green]")
                else:
                    console.print("[bold red]❌ Single translation failed[/bold red]")
                
                # Test language detection
                detected = await translation_service.detect_language(test_text)
                console.print(f"[bold green]✅ Language detection: {detected}[/bold green]")
                
                # Test supported languages
                languages = await translation_service.get_supported_languages()
                console.print(f"[bold green]✅ Supported languages: {len(languages)}[/bold green]")
                
            else:
                console.print("[bold red]❌ Service initialization failed[/bold red]")
        
        await translation_service.close()
        console.print("\n[bold green]🎉 Tests completed![/bold green]")

if __name__ == "__main__":
    test_translation()
