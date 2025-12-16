from skyscope.agents.intelligence import IntelligenceGatherer
from skyscope.agents.simulation import SimulationAgent
from skyscope.reporting.pdf_generator import PDFReportGenerator
from skyscope.video.generator import VideoGenerator
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

console = Console()

class SwarmOrchestrator:
    def __init__(self, query: str, docs_path: str, generate_video: bool):
        self.query = query
        self.docs_path = docs_path
        self.generate_video = generate_video
        self.intelligence_agent = IntelligenceGatherer(docs_path)
        self.simulation_agent = SimulationAgent()
        self.pdf_generator = PDFReportGenerator()
        self.video_generator = VideoGenerator()
        self.context = []
        self.simulation_result = ""
        
    def run(self):
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            # 1. Intelligence Gathering
            task1 = progress.add_task(description="Gathering intelligence from diverse sources...", total=None)
            self.gather_intelligence()
            progress.remove_task(task1)
            
            # 2. Simulation & Strategy
            task2 = progress.add_task(description="Running strategic simulation...", total=None)
            self.run_simulation()
            progress.remove_task(task2)
            
            # 3. Report Generation
            task3 = progress.add_task(description="Compiling PDF report...", total=None)
            self.generate_report()
            progress.remove_task(task3)
            
            # 4. Video Production
            if self.generate_video:
                task4 = progress.add_task(description="Producing video briefing...", total=None)
                self.produce_video()
                progress.remove_task(task4)
                
        console.print("[green]Mission Complete. Artifacts generated.[/green]")

    def gather_intelligence(self):
        console.print(f"[dim]Initialized Intelligence Protocol for: {self.query}[/dim]")
        self.context = self.intelligence_agent.gather(self.query)
        console.print(f"  [dim]- Aggregated {len(self.context)} data points[/dim]")

    def run_simulation(self):
        console.print(f"[dim]Engaging Nemotron Swarm Core...[/dim]")
        self.simulation_result = self.simulation_agent.run_simulation(self.query, self.context)
        console.print("  [dim]- Simulation trajectory calculated[/dim]")
    
    def generate_report(self):
        filename = f"skyscope_report_{int(time.time())}.pdf"
        output_path = self.pdf_generator.generate(filename, self.query, self.simulation_result, self.context)
        console.print(f"  [dim]- Generated classified briefing PDF: {output_path}[/dim]")

    def produce_video(self):
        console.print("[dim]Initiating Video Uplink...[/dim]")
        filename = f"skyscope_briefing_{int(time.time())}.mp4"
        # Use simulation result as script
        output_path = self.video_generator.generate(filename, self.simulation_result)
        if output_path:
            console.print(f"  [dim]- Rendered documentary briefing: {output_path}[/dim]")
        else:
            console.print(f"  [red]- Video generation failed or skipped[/red]")
