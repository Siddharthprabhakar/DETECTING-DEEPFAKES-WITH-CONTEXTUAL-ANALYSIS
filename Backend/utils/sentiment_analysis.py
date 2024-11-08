import moviepy.editor as mp  # For extracting audio from video
import whisper  # For transcribing audio to text using Whisper
from transformers import pipeline
import os

# Load DistilBERT-based sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", framework="pt")

# Initialize the Whisper model for transcription
whisper_model = whisper.load_model("base")  # You can choose other models like "small", "medium", etc.

# Function to extract audio from video
def extract_audio(video_path):
    video = mp.VideoFileClip(video_path)
    if video.audio is None:  # Check if video has audio
        return None
    audio_path = "extracted_audio.wav"
    video.audio.write_audiofile(audio_path)
    return audio_path

# Function to transcribe audio to text using Whisper
def transcribe_audio_with_whisper(audio_path):
    result = whisper_model.transcribe(audio_path)
    return result["text"]

# Function to perform sentiment analysis
def analyze_sentiment(text):
    sentiment_results = sentiment_analyzer(text)
    sentiment_label = sentiment_results[0]['label']
    sentiment_score = sentiment_results[0]['score']

    sentiment_mapping = {
        "LABEL_0": "very negative",
        "LABEL_1": "negative",
        "LABEL_2": "neutral",
        "LABEL_3": "positive",
        "LABEL_4": "very positive"
    }

    sentiment = sentiment_mapping.get(sentiment_label, "neutral")
    return sentiment, sentiment_score

# Main function to process video, extract audio, and analyze sentiment
def analyze_video_sentiment(video_path):
    audio_path = extract_audio(video_path)  # Extract audio from video

    if audio_path is None:
        return None, None, None  # Return None when audio is not available

    transcribed_text = transcribe_audio_with_whisper(audio_path)  # Transcribe audio to text using Whisper

    if transcribed_text:
        sentiment, sentiment_score = analyze_sentiment(transcribed_text)  # Perform sentiment analysis on transcribed text
        return sentiment, sentiment_score, transcribed_text
    else:
        return None, None, None  # In case transcription fails