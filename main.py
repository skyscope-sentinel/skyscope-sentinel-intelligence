import sys
import time
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.text import Text

from skyscope.agents.orchestrator import SwarmOrchestrator
from skyscope.utils.config import Config
from skyscope.utils.model_loader import ensure_models_exist

console = Console()

def make_layout() -> Layout:
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=3)
    )
    layout["main"].split_row(
        Layout(name="metrics", ratio=1),
        Layout(name="output", ratio=2)
    )
    return layout

def update_metrics(layout, metrics_data):
    table = Table(expand=True, border_style="dim")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    
    for k, v in metrics_data.items():
        table.add_row(k, str(v))
        
    layout["metrics"].update(Panel(table, title="System Metrics", border_style="blue"))

def main():
    # 0. Boot Sequence
    console.print(Panel("[bold cyan]INITIALIZING SKYSCOPE SENTINEL INTELLIGENCE CORE...[/bold cyan]", border_style="cyan"))
    ensure_models_exist()
    time.sleep(1)
    
    orchestrator = SwarmOrchestrator(docs_path="./intel", generate_video=True)
    
    # Check for one-shot command
    if len(sys.argv) > 1:
        instruction = " ".join(sys.argv[1:])
        orchestrator.process_instruction(instruction)
        return

    # Interactive Live Mode
    metrics = {
        "Status": "STANDBY",
        "Missions": 0,
        "Agents": 3,
        "Embedded.AI": "ACTIVE"
    }

    # Header
    header = Panel(
        Text("SKYSCOPE SENTINEL | AUTONOMOUS SWARM COLLECTIVE", justify="center", style="bold white"),
        style="on blue"
    )

    while True:
        try:
            # 1. Input Loop (Outside Live to allow typing)
            console.print("\n[bold green]COMMAND REQUEST > [/bold green]", end="")
            instruction = input()
            
            if instruction.lower() in ['exit', 'quit']:
                console.print("[red]Shutting down...[/red]")
                break
            
            if not instruction.strip():
                continue

            # 2. Execution Loop (Inside Live for visuals)
            layout = make_layout()
            layout["header"].update(header)
            
            metrics["Status"] = "PROCESSING"
            metrics["Missions"] += 1
            
            with Live(layout, refresh_per_second=4, screen=False) as live:
                # Update loop for visual feedback
                update_metrics(layout, metrics)
                
                # Mock progress for UI demo (Real logs go to stdout which Rich captures)
                layout["output"].update(Panel(f"[yellow]Executing: {instruction}[/yellow]\n[dim]Dispatching agents...[/dim]", title="Live Feed"))
                live.refresh()
                
                # Run actual logic
                # Note: The Orchestrator uses its own Console, so we might see mixed output
                #Ideally we'd redirect orchestrator output to the panel, but for now we run it directly
                # to ensure the user sees the detailed logs.
                live.stop() 
                
                orchestrator.process_instruction(instruction)
                
                metrics["Status"] = "STANDBY"

        except KeyboardInterrupt:
            console.print("\n[red]Manual Override Disengaged.[/red]")
            break
        except Exception as e:
            console.print(f"[bold red]System Critical:[/bold red] {e}")

if __name__ == "__main__":
    main()
