import whisper
import wave
import numpy as np
import torch

# Initialize Whisper model once to avoid reloading
whisper_model = whisper.load_model("base")

def transcribe_audio_with_whisper(audio_path):
    try:
        print(f"[Transcription] Starting transcription for audio at path: {audio_path}")

        # Load audio data directly from the file using wave (or scipy if needed)
        with wave.open(audio_path, "rb") as audio_file:
            frames = audio_file.readframes(audio_file.getnframes())
            rate = audio_file.getframerate()
            audio_data = np.frombuffer(frames, dtype=np.int16)

        # Convert audio data to Whisper-compatible format
        audio_tensor = torch.FloatTensor(audio_data / 32768.0)  # Normalize to [-1, 1] range
        
        # Perform transcription
        result = whisper_model.transcribe(audio_tensor, language="en")
        transcribed_text = result.get("text", "")
        
        if not transcribed_text:
            print("[Transcription] No text produced; transcription might have failed.")
            return "No transcription text produced"
        
        print(f"[Transcription] Transcription successful. Text: {transcribed_text}")
        return transcribed_text

    except Exception as e:
        print(f"[Transcription] Error during transcription: {str(e)}")
        return "Transcription error"
