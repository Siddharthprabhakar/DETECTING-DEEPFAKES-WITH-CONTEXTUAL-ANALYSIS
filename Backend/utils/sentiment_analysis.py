# emotion_analysis.py
from transformers import pipeline
import speech_recognition as sr
from moviepy.editor import AudioFileClip
import os

# Initialize the emotion detection pipeline
emotion_analyzer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

# Extract audio from video
def extract_audio_from_video(video_path, output_audio_path):
    try:
        audio_clip = AudioFileClip(video_path)
        audio_clip.write_audiofile(output_audio_path, codec='pcm_s16le')
        audio_clip.close()
    except Exception as e:
        print(f"Error extracting audio from video {video_path}: {e}")

# Transcribe audio to text
def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except (sr.UnknownValueError, sr.RequestError):
            return None

# Perform emotion detection
def perform_emotion_detection(text):
    result = emotion_analyzer(text)
    emotion = result[0]['label']
    score = result[0]['score']
    return emotion, score

# Main function for emotion analysis
def analyze_emotion(video_path):
    temp_audio_path = "temp_audio.wav"
    
    # Try extracting audio from the video
    try:
        extract_audio_from_video(video_path, temp_audio_path)
        
        # Try transcribing audio to text
        text = transcribe_audio(temp_audio_path)
        os.remove(temp_audio_path)  # Clean up temporary audio file

        if text:
            emotion, score = perform_emotion_detection(text)
            return emotion, score, text
        else:
            # Return None if transcription failed (likely no audio)
            return None, None, None

    except Exception as e:
        print(f"Error during emotion analysis: {str(e)}")
        return None, None, None  # Return None to indicate audio unavailability
