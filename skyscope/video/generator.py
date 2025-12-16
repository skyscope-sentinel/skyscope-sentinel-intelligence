import os
import time
from moviepy.video.VideoClip import ColorClip, TextClip
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import AudioArrayClip
from elevenlabs.client import ElevenLabs
from ..utils.config import Config

class VideoGenerator:
    def __init__(self, output_dir="."):
        self.output_dir = output_dir
        self.el_client = None
        if Config.ELEVENLABS_API_KEY:
            self.el_client = ElevenLabs(api_key=Config.ELEVENLABS_API_KEY)

    def generate(self, filename: str, script: str):
        """
        Generates a video briefing from the script.
        1. TTS Generation (ElevenLabs)
        2. Visual Synthesis (MoviePy TextClips)
        3. Assembly
        """
        audio_path = self._generate_audio(script)
        if not audio_path:
            return None

        # Create visuals
        # For this simulated environment, we create a simple text-based video
        # In a real heavy-compute env, we would generate images or pick stock footage
        
        try:
            # Create a video clip that matches the audio duration
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            
            # Background
            bg = ColorClip(size=(1280, 720), color=(0, 0, 0), duration=duration)
            
            # Text overlay (Title)
            # Note: TextClip requires ImageMagick. If failing, we fallback to just audio or blank video
            try:
                txt = TextClip("SKYSCOPE CLASSIFIED BRIEFING", font_size=70, color='white', size=(1280, 720))
                txt = txt.set_duration(duration)
                video = concatenate_videoclips([bg, txt], method="compose") # Simplification
            except OSError:
                # ImageMagick likely missing
                video = bg

            video = video.set_audio(audio)
            
            output_path = os.path.join(self.output_dir, filename)
            video.write_videofile(output_path, fps=24)
            return output_path

        except Exception as e:
            print(f"Video generation error: {e}")
            return None

    def _generate_audio(self, text: str) -> str:
        """
        Generates audio using ElevenLabs or a mock if key is missing.
        """
        snippet = text[:500] # Limit for demo
        out_path = "temp_audio.mp3"
        
        if self.el_client:
            try:
                # Casey Jay Topojani voice or default
                # We'll use a standard pre-made voice ID for now if specific one isn't known
                audio = self.el_client.generate(
                    text=snippet,
                    voice="Rachel",
                    model="eleven_multilingual_v2"
                )
                with open(out_path, "wb") as f:
                    for chunk in audio:
                        f.write(chunk)
                return out_path
            except Exception as e:
                print(f"ElevenLabs error: {e}")
                return self._mock_audio(out_path)
        else:
            return self._mock_audio(out_path)
            
    def _mock_audio(self, path: str) -> str:
        # Create a silent or dummy audio file if real TTS is not available
        # Using moviepy to generate silence
        from moviepy.audio.AudioClip import AudioArrayClip
        import numpy as np
        
        # 5 seconds of silence/noise
        rate = 44100
        duration = 5
        audio_array = np.zeros((rate * duration, 2))
        clip = AudioArrayClip(audio_array, fps=rate)
        clip.write_audiofile(path)
        return path
