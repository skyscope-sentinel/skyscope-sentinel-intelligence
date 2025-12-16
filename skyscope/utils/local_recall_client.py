import requests
import os
from .config import Config

class LocalRecallClient:
    def __init__(self):
        self.base_url = Config.LOCALRECALL_BASE_URL.rstrip('/')
        # Ensure base URL points to the API root if not configured that way
        if not self.base_url.endswith("/api"):
            # The config default is ...:8081/api, but if user overrides with base domain
            pass 

    def create_collection(self, name: str) -> bool:
        """Creates a new collection in LocalRecall."""
        try:
            url = f"{self.base_url}/collections"
            response = requests.post(url, json={"name": name})
            return response.status_code in [200, 201]
        except Exception as e:
            print(f"LocalRecall Error (Create Collection): {e}")
            return False

    def upload_file(self, collection_name: str, file_path: str) -> bool:
        """Uploads a file to the specified collection."""
        try:
            url = f"{self.base_url}/collections/{collection_name}/upload"
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f)}
                response = requests.post(url, files=files)
            return response.status_code == 200
        except Exception as e:
            print(f"LocalRecall Error (Upload File): {e}")
            return False

    def search(self, collection_name: str, query: str, limit: int = 5) -> list:
        """Searches the collection for relevant snippets."""
        try:
            url = f"{self.base_url}/collections/{collection_name}/search"
            response = requests.post(url, json={"query": query, "max_results": limit})
            if response.status_code == 200:
                # Response format depends on LocalRecall version, assuming standard list of results
                results = response.json()
                return results if isinstance(results, list) else results.get('results', [])
            return []
        except Exception as e:
            print(f"LocalRecall Error (Search): {e}")
            return []

    def list_collections(self) -> list:
        """Lists available collections."""
        try:
            url = f"{self.base_url}/collections"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            # print(f"LocalRecall Error (List config): {e}") # Silent fail often better for logic checks
            return []
