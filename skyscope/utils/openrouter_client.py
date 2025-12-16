import json
import requests
import os
from .config import Config

class OpenRouterClient:
    def __init__(self, model_name: str = "nvidia/nemotron-nano-12b-v2-vl:free"):
        self.api_key = Config.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"
        self.model_name = model_name
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://github.com/skyscope-sentinel", # Site URL for rankings
            "X-Title": "Skyscope Sentinel Swarm", # Site title for rankings
            "Content-Type": "application/json"
        }

    def chat_completion(self, messages: list, temperature: float = 0.7) -> str:
        """
        Sends a chat completion request to OpenRouter.
        """
        if not self.api_key:
            print("[Warning] No OPENROUTER_API_KEY found. Client is disabled.")
            return "Reference Code 0x0: OpenRouter Uplink Failed."

        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
            # Optional: Add tools, response_format, etc. here if needed later
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                data=json.dumps(payload),
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            
            # Extract content from choices
            if 'choices' in data and len(data['choices']) > 0:
                return data['choices'][0]['message']['content']
            return ""
            
        except Exception as e:
            print(f"[Error] OpenRouter Request Failed: {e}")
            return f"Error: {str(e)}"

    def get_models(self):
        """
        Fetches available models to verify connectivity.
        """
        try:
            response = requests.get(f"{self.base_url}/models", headers=self.headers)
            return response.json()
        except Exception as e:
            print(f"[Error] Failed to fetch models: {e}")
            return {}
