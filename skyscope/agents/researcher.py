import os
from typing import List, Dict
try:
    import trafilatura
except ImportError:
    trafilatura = None
try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    YouTubeTranscriptApi = None

from ..utils.local_recall_client import LocalRecallClient

class ResearcherAgent:
    def __init__(self, docs_path: str = None, collection_name="skyscope_intel"):
        self.docs_path = docs_path
        self.collection_name = collection_name
        self.recall_client = LocalRecallClient()
        self.sources = []

    def conduct_research(self, instruction: str) -> List[Dict]:
        """
        Executes a deep search. 
        Auto-detects URLs in the instruction effectively acting as a 'Browse' tool.
        """
        print(f"  [Researcher] Analyzing directives: {instruction[:50]}...")
        findings = []

        # 1. Autonomous Scraping (RT.com / News)
        if "http" in instruction:
            urls = [word for word in instruction.split() if word.startswith("http")]
            for url in urls:
                if "youtube.com" in url or "youtu.be" in url:
                    video_data = self._get_youtube_transcript(url)
                    if video_data:
                        findings.append(video_data)
                else:
                    web_data = self._scrape_url(url)
                    if web_data:
                        findings.append(web_data)
        
        # 2. LocalRecall Search
        # Ingest local documents if they exist
        if self.docs_path and os.path.exists(self.docs_path):
             self.recall_client.create_collection(self.collection_name)
             self._ingest_docs()
        
        # Search existing knowledge
        results = self.recall_client.search(self.collection_name, instruction, limit=5)
        if results:
            for item in results:
                text = item.get('text') or item.get('content') or str(item)
                source = item.get('file') or item.get('metadata', {}).get('source', 'Unknown')
                findings.append({"source": f"LocalMemory ({source})", "content": text[:800]})
        
        # 3. Fallback Simulation (if no real data found)
        if not findings:
            print("  [Researcher] No live/local data found. Engaging simulation protocol.")
            findings.append({
                "source": "Simulation Node", 
                "content": f"Simulated context suggesting high volatility regarding '{instruction}' based on historical patterns."
            })
            
        return findings

    def _scrape_url(self, url: str) -> Dict:
        """Uses Trafilatura to extract text from news sites."""
        if not trafilatura:
            return {"source": "System", "content": "Trafilatura library not installed."}
        
        print(f"  [Researcher] Scraping target: {url}")
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                text = trafilatura.extract(downloaded)
                if text:
                    return {"source": f"WebScrape ({url})", "content": text[:2000]} # Limit context
        except Exception as e:
            print(f"  [Researcher] Scraping failed: {e}")
        return None

    def _get_youtube_transcript(self, url: str) -> Dict:
        """Uses youtube-transcript-api to get video text."""
        if not YouTubeTranscriptApi:
             return {"source": "System", "content": "YouTube Transcript API not installed."}
             
        try:
            video_id = url.split("v=")[-1].split("&")[0]
            print(f"  [Researcher] Extracting transcript for Video ID: {video_id}")
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            full_text = " ".join([entry['text'] for entry in transcript])
            return {"source": f"YouTube ({video_id})", "content": full_text[:2000]}
        except Exception as e:
            print(f"  [Researcher] Transcript extraction failed: {e}")
        return None

    def _ingest_docs(self):
        """Walks the doc path and uploads supported files to LocalRecall."""
        if not self.docs_path: return
        for root, _, files in os.walk(self.docs_path):
            for file in files:
                if file.lower().endswith(('.pdf', '.txt', '.md')):
                    path = os.path.join(root, file)
                    self.recall_client.upload_file(self.collection_name, path)
