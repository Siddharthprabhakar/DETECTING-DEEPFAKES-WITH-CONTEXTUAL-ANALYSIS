from flask import Flask, request, jsonify, Response, stream_with_context
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import time
from utils.deepfake_video import detect_fake_video
from utils.Sentiment_analysis.audio_extraction import extract_audio
from utils.Sentiment_analysis.transcription import transcribe_audio_with_whisper
from utils.Sentiment_analysis.sentiment_analysis import analyze_sentiment

UPLOAD_FOLDER = 'Uploaded_Files'
AUDIO_FOLDER = 'Audio_Files'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Enable CORS
CORS(app, resources={r"/Detect": {"origins": "http://localhost:3000"}, r"/progress/*": {"origins": "http://localhost:3000"}})

# Streaming progress function
def stream_progress(video_path):
    total_steps = 100
    for i in range(total_steps):
        time.sleep(0.1)
        progress = i + 1
        estimated_time_left = (total_steps - progress) * 0.1
        yield f"data: {progress},{estimated_time_left}\n\n"

@app.route('/progress/<filename>', methods=['GET'])
def progress(filename):
    video_path = f"Uploaded_Files/{filename}"
    return Response(stream_with_context(stream_progress(video_path)), mimetype='text/event-stream')

# Helper function for sentiment analysis
def analyze_video_sentiment(video_path):
    try:
        print(f"[Video Sentiment Analysis] Starting sentiment analysis for video: {video_path}")

        # Extract audio
        audio_path = extract_audio(video_path)
        if not audio_path:
            print("[Video Sentiment Analysis] No audio extracted; skipping sentiment analysis.")
            return "N/A", "N/A", "No audio available"

        # Transcribe audio to text
        transcribed_text = transcribe_audio_with_whisper(audio_path)
        if not transcribed_text:
            print("[Video Sentiment Analysis] Transcription failed; skipping sentiment analysis.")
            return "N/A", "N/A", "Transcription error"

        # Analyze sentiment
        sentiment, sentiment_score = analyze_sentiment(transcribed_text)
        print(f"[Video Sentiment Analysis] Completed with sentiment: {sentiment}, score: {sentiment_score}")
        return sentiment, sentiment_score, transcribed_text

    except Exception as e:
        print(f"[Video Sentiment Analysis] Error during sentiment analysis: {str(e)}")
        return "N/A", "N/A", "Sentiment analysis error"

@app.route('/Detect', methods=['POST'])
def DetectPage():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file uploaded'}), 400

    video = request.files['video']
    video_filename = secure_filename(video.filename)
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    video.save(video_path)

    if not os.path.exists(video_path):
        return jsonify({'error': 'File upload failed'}), 500
    else:
        print(f"[DetectPage] File uploaded successfully: {video_path}")

    try:
        prediction = detect_fake_video(video_path)
        is_fake = prediction[0] == 0
        output = "FAKE" if is_fake else "REAL"
        confidence = prediction[1]

        # Perform sentiment analysis regardless of deepfake status
        sentiment, sentiment_score, transcribed_text = analyze_video_sentiment(video_path)
        emotion_analysis_result = {
            'emotion': sentiment,
            'score': sentiment_score,
            'transcribed_text': transcribed_text
        }

        # Cleanup
        if os.path.exists(video_path):
            try:
                os.remove(video_path)
            except PermissionError as e:
                print(f"[DetectPage] Could not delete video file immediately: {e}")
                time.sleep(1)
                os.remove(video_path)

        response = {
            'deepfake_result': {
                'result': output,
                'confidence': confidence
            },
            'emotion_result': emotion_analysis_result
        }

        print("Response to frontend:", response)
        return jsonify(response), 200

    except Exception as e:
        print(f"[DetectPage] Error during detection: {str(e)}")
        return jsonify({'error': 'Error during detection'}), 500

if __name__ == '__main__':
    app.run(port=5000)
