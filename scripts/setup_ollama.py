"""
Setup script for Ollama and translation models
"""
import asyncio
import click
import logging
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from utils.ollama_client import OllamaClient
from utils.config import config

console = Console()
logging.basicConfig(level=logging.INFO)

@click.command()
@click.option('--model', '-m', default='nllb-200', help='Model to install')
@click.option('--check', '-c', is_flag=True, help='Check Ollama status')
@click.option('--list', '-l', is_flag=True, help='List available models')
def setup_ollama(model, check, list_models):
    """Setup Ollama and translation models"""
    
    async def run_async():
        console.print(Panel("🔧 Ollama Setup for Language Translation", style="bold blue"))
        
        ollama_client = OllamaClient()
        
        # Check Ollama status
        if check or list_models:
            console.print("\n[bold yellow]Checking Ollama status...[/bold yellow]")
            
            if await ollama_client.is_available():
                console.print("[bold green]✅ Ollama is running[/bold green]")
                
                if list_models:
                    models = await ollama_client.list_models()
                    if models:
                        console.print(f"\n[bold cyan]Available models:[/bold cyan]")
                        for model_name in models:
                            console.print(f"  • {model_name}")
                    else:
                        console.print("[yellow]No models installed[/yellow]")
            else:
                console.print("[bold red]❌ Ollama is not running[/bold red]")
                console.print("\n[yellow]Please install and start Ollama:[/yellow]")
                console.print("  [green]curl -fsSL https://ollama.ai/install.sh | sh[/green]")
                console.print("  [green]ollama serve[/green]")
                return
        
        # Install model
        if model:
            console.print(f"\n[bold yellow]Installing model: {model}[/bold yellow]")
            
            if not await ollama_client.is_available():
                console.print("[bold red]❌ Ollama is not available[/bold red]")
                return
            
            # Check if model is supported
            if model not in config.SUPPORTED_MODELS:
                console.print(f"[bold red]❌ Model {model} is not supported[/bold red]")
                console.print(f"Supported models: {list(config.SUPPORTED_MODELS.keys())}")
                return
            
            model_config = config.SUPPORTED_MODELS[model]
            model_name = model_config['name']
            
            console.print(f"[cyan]Model: {model_name}[/cyan]")
            console.print(f"[cyan]Size: {model_config['size']}[/cyan]")
            console.print(f"[cyan]Provider: {model_config['provider']}[/cyan]")
            
            # Check if already installed
            installed_models = await ollama_client.list_models()
            if model_name in installed_models:
                console.print(f"[bold green]✅ Model {model_name} is already installed[/bold green]")
                return
            
            # Install model
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task(f"Installing {model_name}...", total=None)
                
                success = await ollama_client.pull_model(model_name)
                
                if success:
                    progress.update(task, description=f"[bold green]✅ {model_name} installed successfully[/bold green]")
                    console.print(f"\n[bold green]🎉 Model installation completed![/bold green]")
                    console.print(f"\n[cyan]You can now use the translation service with:[/cyan]")
                    console.print(f"  [green]python main.py --interactive[/green]")
                else:
                    progress.update(task, description=f"[bold red]❌ Failed to install {model_name}[/bold red]")
                    console.print(f"\n[bold red]❌ Model installation failed[/bold red]")

if __name__ == "__main__":
    setup_ollama()
