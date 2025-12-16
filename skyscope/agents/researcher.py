import os
from typing import List, Dict
from ..utils.local_recall_client import LocalRecallClient

class ResearcherAgent:
    def __init__(self, docs_path: str = None, collection_name="skyscope_intel"):
        self.docs_path = docs_path
        self.collection_name = collection_name
        self.recall_client = LocalRecallClient()
        self.sources = []

    def conduct_research(self, instruction: str) -> List[Dict]:
        """
        Executes a deep search based on the instruction.
        1. Checks LocalRecall for existing data.
        2. Ingests new local files if docs_path is provided.
        # Future: Call MCP tools for web search (not yet implemented)
        """
        print(f"  [Researcher] Searching deeply for: {instruction}")
        
        # 1. Ingest local documents if they exist (Refresh knowledge)
        if self.docs_path and os.path.exists(self.docs_path):
            self.recall_client.create_collection(self.collection_name)
            self._ingest_docs()
            
        # 2. Search LocalRecall for context
        results = self.recall_client.search(self.collection_name, instruction, limit=10)
        
        # 3. Format results
        findings = []
        if results:
            for item in results:
                text = item.get('text') or item.get('content') or str(item)
                source = item.get('file') or item.get('metadata', {}).get('source', 'Unknown')
                findings.append({"source": f"LocalRecall ({source})", "content": text[:800]})
        else:
            # Fallback / Simulation of "Deep Web Search"
            print("  [Researcher] Local data insufficient. Engaging deep web simulation protocol.")
            findings = [
                {"source": "Simulation Node A", "content": f"Simulated deep web hit for {instruction[:20]}... indicating high volatility."},
                {"source": "Simulation Node B", "content": f"Cross-referenced historical data suggests cyclical pattern regarding {instruction[:20]}..."},
            ]
            
        return findings

    def _ingest_docs(self):
        """
        Walks the doc path and uploads supported files to LocalRecall.
        """
        count = 0
        for root, _, files in os.walk(self.docs_path):
            for file in files:
                if file.lower().endswith(('.pdf', '.txt', '.md')):
                    path = os.path.join(root, file)
                    if self.recall_client.upload_file(self.collection_name, path):
                        count += 1
        if count > 0:
            print(f"  [Researcher] Ingested {count} new local documents.")
