from ..utils.openrouter_client import OpenRouterClient

class AnalystAgent:
    def __init__(self):
        self.client = OpenRouterClient()
        
    def analyze(self, query: str, raw_intelligence: list) -> str:
        """
        Synthesizes raw intelligence into a critical assessment.
        """
        # Format context
        context_str = "\n".join([f"- {item.get('content', '')}" for item in raw_intelligence])
        
        system_prompt = """You are a Deep Insights Analyst for Skyscope Sentinel. 
        Your role is to apply critical theory and strategic analysis to raw intelligence.
        Do not just summarize; identify patterns, contradictions, and high-probability trajectories.
        Focus on:
        1. Economic & Financial vectors.
        2. Historical precedence (blood & land).
        3. Hidden political alignments.
        """
        
        user_prompt = f"""
        QUERY: {query}
        
        RAW INTELLIGENCE:
        {context_str}
        
        TASK:
        Provide a "Critical Assessment" of the situation. 
        Highlight key risks and 2-3 likely future scenarios.
        """
        
        return self.client.chat_completion([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])
