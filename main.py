#!/usr/bin/env python3
import argparse
import sys
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

from skyscope.agents.orchestrator import SwarmOrchestrator

load_dotenv()
console = Console()

def main():
    parser = argparse.ArgumentParser(description="Skyscope Swarm Intelligence System")
    parser.add_argument("query", nargs="?", help="The intelligence query to simulate")
    parser.add_argument("--docs", default="./docs", help="Path to local documents for context")
    parser.add_argument("--video", action="store_true", help="Generate video report")
    
    args = parser.parse_args()

    if not args.query:
        console.print(Panel("Welcome to Skyscope Sentinel Intelligence. Please provide a query.", title="Skyscope", style="blue"))
        sys.exit(0)

    console.print(Panel(f"Initializing Swarm for query: [bold]{args.query}[/bold]", title="Skyscope Active", style="green"))

    orchestrator = SwarmOrchestrator(
        query=args.query,
        docs_path=args.docs,
        generate_video=args.video
    )
    
    try:
        orchestrator.run()
    except Exception as e:
        console.print(f"[red]Error during execution:[/red] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
