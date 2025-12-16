from openai import OpenAI
from ..utils.config import Config

class SimulationAgent:
    def __init__(self):
        self.client = None
        if Config.OPENROUTER_API_KEY:
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=Config.OPENROUTER_API_KEY,
            )

    def run_simulation(self, query: str, context: list) -> str:
        """
        Runs the strategic simulation using the specified model.
        """
        if not self.client:
            return "Simulation skipped: No OpenRouter API Key provided."

        # Construct a prompt that enforces the persona and strict constraints
        prompt = f"""
        You are SKYSCOPE SENTINEL INTELLIGENCE.
        Query: {query}
        Context: {context}
        
        Perform a high-level strategic simulation considering:
        1. Economic & Financial Systems (Trade routes, benefits, land worth)
        2. Technological Supremacy
        3. Geographical & Historical Factors (Blood lost, sacrifices)
        4. Political Posturing & Alignments
        
        Leverage multi-perspective analysis (Western, Russian, Arabic, etc.).
        
        Output a detailed strategic trajectory report.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=Config.MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a highly advanced strategic AI simulator."},
                    {"role": "user", "content": prompt}
                ],
                extra_headers={
                    "HTTP-Referer": "https://skyscope.ai", # Required by OpenRouter
                    "X-Title": "Skyscope",
                },
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Simulation failed: {str(e)}"
