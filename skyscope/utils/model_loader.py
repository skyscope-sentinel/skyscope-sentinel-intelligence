import os
import requests
from pathlib import Path
from rich.console import Console

console = Console()

MODELS_DIR = Path("models")

MODELS = {
    "qwen": {
        "url": "https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q4_k_m.gguf",
        "filename": "qwen2.5-0.5b-instruct.gguf",
        "desc": "Logic Core (Qwen2.5-0.5B)"
    },
    "kokoro": {
        "url": "https://huggingface.co/hexgrad/Kokoro-82M/resolve/main/kokoro.onnx", # Placeholder - usually needs weights + config
        # For simplicity in this demo, accessing specific ONNX file location if available or using kokoro-onnx lib auto-download
        "filename": "kokoro-v0_19.onnx", 
        "desc": "Voice Synthesis (Kokoro-82M)"
    }
}

def ensure_models_exist():
    """
    Checks for presence of embedded models and downloads them if missing.
    """
    if not MODELS_DIR.exists():
        MODELS_DIR.mkdir(parents=True)
        
    console.print("[dim]Verifying Embedded Neural Array...[/dim]")
    
    for key, model in MODELS.items():
        path = MODELS_DIR / model["filename"]
        if not path.exists():
            console.print(f"[yellow]  - Downloading {model['desc']}...[/yellow]")
            try:
                # In a real scenario, use huggingface_hub for more robust handling
                # or requests for direct GGUF
                response = requests.get(model["url"], stream=True)
                response.raise_for_status()
                with open(path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                console.print(f"[green]  - {model['desc']} Online.[/green]")
            except Exception as e:
                console.print(f"[red]  - Failed to acquire {model['desc']}: {e}[/red]")
        else:
             console.print(f"[dim]  - {model['desc']} Verified.[/dim]")

if __name__ == "__main__":
    ensure_models_exist()
