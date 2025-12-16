import os
from typing import List, Dict
from ..utils.local_recall_client import LocalRecallClient

class IntelligenceGatherer:
    def __init__(self, docs_path: str, collection_name="skyscope_intel"):
        self.docs_path = docs_path
        self.collection_name = collection_name
        self.recall_client = LocalRecallClient()
        self.sources = []

    def gather(self, query: str) -> List[Dict]:
        """
        Gathers intelligence by scanning local docs (ingesting to LocalRecall) 
        and searching for relevant context.
        """
        # 1. Ingest local documents if they exist
        if self.docs_path and os.path.exists(self.docs_path):
            self.recall_client.create_collection(self.collection_name)
            self._ingest_docs()
            
        # 2. Search LocalRecall for context
        results = self.recall_client.search(self.collection_name, query, limit=5)
        
        # 3. Format results
        config_context = []
        if results:
            for item in results:
                # LocalRecall results structure extraction
                text = item.get('text') or item.get('content') or str(item)
                source = item.get('file') or item.get('metadata', {}).get('source', 'Unknown')
                config_context.append({"source": source, "content": text[:500] + "..."})
        else:
            # Fallback simulations if nothing found
            config_context = [
                {"source": "Intelligence Node 1", "content": "Monitoring open source channels... (No local context found)"},
                {"source": "Intelligence Node 2", "content": "Intercepting regional communications... (No local context found)"},
            ]
            
        return config_context

    def _ingest_docs(self):
        """
        Walks the doc path and uploads supported files to LocalRecall.
        """
        for root, _, files in os.walk(self.docs_path):
            for file in files:
                if file.lower().endswith(('.pdf', '.txt', '.md')):
                    path = os.path.join(root, file)
                    # We might want to avoid re-uploading every time in production,
                    # but for this swarm session we ensure fresh intel.
                    # LocalRecall likely handles dedup or overwrite.
                    self.recall_client.upload_file(self.collection_name, path)
