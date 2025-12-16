import os
from dotenv import load_dotenv

# Load .env but do not overwrite existing environment variables (default behavior of load_dotenv is override=False)
load_dotenv()

class Config:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    LOCALAI_BASE_URL = os.getenv("LOCALAI_BASE_URL", "http://localhost:8080/v1")
    LOCALAI_TTS_URL = os.getenv("LOCALAI_TTS_URL", "http://localhost:8080/tts")
    
    # LocalRecall runs on port 8081 in our docker-compose
    LOCALRECALL_BASE_URL = os.getenv("LOCALRECALL_BASE_URL", "http://localhost:8081/api")
    
    # LocalAGI ran on port 3000
    LOCALAGI_BASE_URL = os.getenv("LOCALAGI_BASE_URL", "http://localhost:3000")

    MCP_CONFIG_PATH = os.getenv("MCP_CONFIG_PATH", "./untitled.txt")
    
    MODEL_NAME = "nvidia/nemotron-nano-12b-v2-vl:free" # Remote
    LOCAL_MODEL_NAME = "gpt-4" # LocalAI often maps requests to loaded model regardless of name, or use specific local model name
    
    @classmethod
    def validate(cls):
        missing = []
        # We don't error on missing keys now, as we have fallbacks
        if not cls.OPENROUTER_API_KEY:
            # Check if LocalAI is reachable? (Optional)
            pass
        return missing
