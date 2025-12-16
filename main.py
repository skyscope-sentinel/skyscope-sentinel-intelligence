import sys
from skyscope.agents.orchestrator import SwarmOrchestrator
from skyscope.utils.config import Config
from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
    # Banner
    console.print(Panel.fit(
        "[bold cyan]SKYSCOPE SENTINEL INTELLIGENCE[/bold cyan]\n[dim]Autonomous Geopolitical Swarm Collective[/dim]",
        border_style="cyan"
    ))
    
    # Check for arguments (e.g. `skyscope "Run simulation on X"`)
    if len(sys.argv) > 1:
        instruction = " ".join(sys.argv[1:])
    else:
        # Fallback to REPL / Interactive Mode
        console.print("[yellow]No instruction provided. Entering Interactive Mode.[/yellow]")
        instruction = console.input("[bold green]Enter Directive > [/bold green]")
        
    if not instruction:
        console.print("[red]Empty instruction. Aborting.[/red]")
        return

    # Initialize Orchestrator
    # We default docs_path to current directory or a specific 'intel' folder if it exists
    orchestrator = SwarmOrchestrator(docs_path="./intel", generate_video=True)
    
    try:
        orchestrator.process_instruction(instruction)
    except KeyboardInterrupt:
        console.print("\n[red]Mission Aborted by User.[/red]")
    except Exception as e:
        console.print(f"\n[bold red]Critical System Failure:[/bold red] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
