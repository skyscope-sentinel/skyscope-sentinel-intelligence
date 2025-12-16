import os
import soundfile as sf
from pathlib import Path

# Try importing kokoro-onnx, handle missing dep gracefully
try:
    from kokoro_onnx import Kokoro
except ImportError:
    Kokoro = None

class TTSEngine:
    def __init__(self, models_dir="models"):
        self.models_dir = Path(models_dir)
        self.kokoro = None
        self._init_kokoro()

    def _init_kokoro(self):
        """Initialize Kokoro ONNX session if model exists."""
        model_path = self.models_dir / "kokoro-v0_19.onnx"
        voices_path = self.models_dir / "voices.json" # Hypothetical voices config
        
        if Kokoro and model_path.exists():
            try:
                # In real usage, you'd download voices.json too. 
                # passing model path. 
                self.kokoro = Kokoro(str(model_path), str(voices_path)) 
                print("[TTS] Kokoro-82M High-Fidelity Engine Initialized.")
            except Exception as e:
                print(f"[TTS] Kokoro Init Failed (Fallback inactive): {e}")

    def generate_audio(self, text: str, output_path: str) -> bool:
        """
        Generates audio using Kokoro if available, otherwise returns False 
        (VideoGenerator should then try ElevenLabs/LocalAI).
        """
        if self.kokoro:
            try:
                # Generate audio (returns numpy array, sample_rate)
                # Using a default voice style "af_sarah" or similar
                audio, sample_rate = self.kokoro.create(text, voice="af_sarah", speed=1.0)
                
                # Save to file
                sf.write(output_path, audio, sample_rate)
                return True
            except Exception as e:
                print(f"[TTS] Kokoro Generation Error: {e}")
                return False
        return False
