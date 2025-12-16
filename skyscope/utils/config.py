import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    MCP_CONFIG_PATH = os.getenv("MCP_CONFIG_PATH", "./untitled.txt")
    
    MODEL_NAME = "nvidia/nemotron-nano-12b-v2-vl:free" # As requested
    
    @classmethod
    def validate(cls):
        missing = []
        if not cls.OPENROUTER_API_KEY:
            missing.append("OPENROUTER_API_KEY")
        return missing
