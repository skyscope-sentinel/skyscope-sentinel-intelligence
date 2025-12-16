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
                txt = TextClip(text="SKYSCOPE CLASSIFIED BRIEFING", font_size=70, color='white', size=(1280, 720))
                txt = txt.with_duration(duration)
                video = concatenate_videoclips([bg, txt], method="compose") # Simplification
            except OSError:
                # ImageMagick likely missing
                video = bg

            video = video.with_audio(audio)
            
            output_path = os.path.join(self.output_dir, filename)
            video.write_videofile(output_path, fps=24)
            return output_path

        except Exception as e:
            print(f"Video generation error: {e}")
            return None

    def _generate_audio(self, text: str) -> str:
        """
        Generates audio using ElevenLabs, LocalAI, or a mock if all else fails.
        """
        snippet = text[:500] # Limit for demo
        out_path = "temp_audio.mp3"
        
        # 1. Try ElevenLabs
        if self.el_client:
            try:
                audio = self.el_client.generate(
                    text=snippet,
                    voice="Rachel",
                    model="eleven_multilingual_v2"
                )
                self._save_audio_stream(audio, out_path)
                return out_path
            except Exception as e:
                print(f"ElevenLabs error: {e}. Falling back to LocalAI...")
        
        # 2. Try LocalAI TTS
        if Config.LOCALAI_TTS_URL:
            try:
                import requests
                # OpenAI-compatible TTS endpoint usually /v1/audio/speech but user doc mentions http://localhost:8080/v1/audio/speech
                # Using the config variable which defaults to /tts but let's align with OpenAI standard if possible or use the user provided example.
                # User example: http://localhost:8080/v1/audio/speech
                
                # We'll use the OpenAI client for LocalAI TTS as it's cleaner
                from openai import OpenAI
                local_client = OpenAI(base_url=Config.LOCALAI_BASE_URL, api_key="sk-xxx")
                
                response = local_client.audio.speech.create(
                    model="tts-1",
                    voice="alloy",
                    input=snippet
                )
                response.stream_to_file(out_path)
                return out_path
            except Exception as e:
                print(f"LocalAI TTS error: {e}. Falling back to mock...")

        # 3. Fallback to Mock
        return self._mock_audio(out_path)

    def _save_audio_stream(self, audio_stream, path):
         with open(path, "wb") as f:
            for chunk in audio_stream:
                f.write(chunk)

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
