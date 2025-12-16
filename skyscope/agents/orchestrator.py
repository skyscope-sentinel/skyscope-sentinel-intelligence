import time
import json
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..utils.openrouter_client import OpenRouterClient
from .researcher import ResearcherAgent
from .analyst import AnalystAgent
from .simulation import SimulationAgent
from ..reporting.pdf_generator import PDFReportGenerator
from ..video.generator import VideoGenerator

console = Console()

class SwarmOrchestrator:
    def __init__(self, docs_path: str = None, generate_video: bool = True):
        self.client = OpenRouterClient()
        self.docs_path = docs_path
        self.generate_video = generate_video
        
        # Swarm Collective
        self.researcher = ResearcherAgent(docs_path)
        self.analyst = AnalystAgent()
        self.simulator = SimulationAgent()
        
        # Tools
        self.pdf_generator = PDFReportGenerator()
        self.video_generator = VideoGenerator()

    def process_instruction(self, instruction: str):
        """
        Main entry point for Natural Language Instructions.
        1. Parse instruction -> Blueprint
        2. Execute Blueprint (Research -> Analysis -> Sim -> Report)
        """
        console.print(f"\n[bold green]Skyscope Swarm Active.[/bold green]")
        console.print(f"[dim]Received Instruction: {instruction}[/dim]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            
            # Phase 1: Strategic Blueprinting (Orchestrator Logic)
            task_plan = progress.add_task("[cyan]Orchestrator: Decomposing objectives...[/cyan]", total=None)
            blueprint = self._create_blueprint(instruction)
            progress.remove_task(task_plan)
            console.print(f"[bold cyan]Mission Blueprint:[/bold cyan] {blueprint.get('mission_name', 'Unknown')}")
            
            # Phase 2: Deep Research
            task_res = progress.add_task("[yellow]Researcher: Executing deep search...[/yellow]", total=None)
            raw_intel = self.researcher.conduct_research(blueprint.get('research_directives', instruction))
            progress.remove_task(task_res)
            console.print(f"  [yellow]- Acquired {len(raw_intel)} verified intelligence vectors.[/yellow]")
            
            # Phase 3: Critical Analysis
            task_ana = progress.add_task("[magenta]Analyst: Synthesizing insights...[/magenta]", total=None)
            deep_insights = self.analyst.analyze(instruction, raw_intel)
            progress.remove_task(task_ana)
            console.print(f"  [magenta]- Critical assessment complete.[/magenta]")

            # Phase 4: Simulation & Projection
            task_sim = progress.add_task("[blue]Simulator: Running trajectories...[/blue]", total=None)
            # Pass the insights as context to the simulation
            trajectory = self.simulator.run_simulation(instruction, [{"content": deep_insights, "source": "Skyscope Analyst Swarm"}])
            progress.remove_task(task_sim)
            console.print(f"  [blue]- Trajectory simulation finalized.[/blue]")
            
            # Phase 5: Artifact Generation
            task_art = progress.add_task("[green]Publishing classified artifacts...[/green]", total=None)
            self._generate_artifacts(instruction, deep_insights, trajectory)
            progress.remove_task(task_art)
            
        console.print("\n[bold green]Mission Complete. Swarm entering standby.[/bold green]")

    def _create_blueprint(self, instruction: str) -> dict:
        """
        Uses the Orchestrator LLM to parse the raw instruction into structured directives.
        """
        prompt = f"""
        You are the Swarm Orchestrator. 
        Analyze this incoming command: "{instruction}"
        
        Output a JSON blueprint with:
        - "mission_name": Short title.
        - "research_directives": Specific search query for the Researcher.
        - "simulation_focus": Key variable to simulate.
        """
        response = self.client.chat_completion([
             {"role": "system", "content": "You are a JSON-only planner."},
             {"role": "user", "content": prompt}
        ])
        
        try:
            # Clean possible markdown fencing
            clean_json = response.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except:
            return {
                "mission_name": "General Directive",
                "research_directives": instruction,
                "simulation_focus": "General Outcome"
            }

    def _generate_artifacts(self, query, insights, trajectory):
        timestamp = int(time.time())
        # PDF
        pdf_name = f"skyscope_report_{timestamp}.pdf"
        # We package insights as list of dicts for the existing PDF generator
        intel_context = [{"source": "Analyst Insight", "content": insights}]
        self.pdf_generator.generate(pdf_name, query, trajectory, intel_context)
        console.print(f"  [dim]- PDF Report: {pdf_name}[/dim]")
        
        # Video
        if self.generate_video:
            vid_name = f"skyscope_briefing_{timestamp}.mp4"
            self.video_generator.generate(vid_name, trajectory)
            console.print(f"  [dim]- Video Briefing: {vid_name}[/dim]")
