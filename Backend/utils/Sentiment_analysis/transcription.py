import whisper
import wave
import numpy as np
import torch
from scipy.io import wavfile
from scipy.signal import resample

# Load a larger Whisper model for potentially better accuracy
whisper_model = whisper.load_model("medium")

def transcribe_audio_with_whisper(audio_path):
    try:
        print(f"[Transcription] Starting transcription for audio at path: {audio_path}")

        # Open audio file and verify its duration
        with wave.open(audio_path, "rb") as audio_file:
            sample_rate = audio_file.getframerate()
            num_frames = audio_file.getnframes()
            duration = num_frames / sample_rate
            if duration < 1.0:  # Skip very short audio segments
                print("[Transcription] Audio duration too short for transcription.")
                return "Audio too short for transcription"
            
            # Read and normalize audio data
            frames = audio_file.readframes(num_frames)
            audio_data = np.frombuffer(frames, dtype=np.int16)

        # Resample if necessary to 16 kHz
        if sample_rate != 16000:
            print(f"[Transcription] Resampling audio from {sample_rate} Hz to 16000 Hz")
            audio_data = resample(audio_data, int(len(audio_data) * 16000 / sample_rate))
            sample_rate = 16000
        
        # Normalize and convert to tensor
        audio_tensor = torch.FloatTensor(audio_data / 32768.0)  # Normalize [-1, 1] range

        # Perform transcription with Whisper
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
