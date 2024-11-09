from flask import Flask, request, jsonify, Response, stream_with_context
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import time
from utils.deepfake_video import detect_fake_video
from utils.deepfake_image import detect_fake_image  # Assuming image detection function is in this file
from utils.Sentiment_analysis.audio_extraction import extract_audio
from utils.Sentiment_analysis.transcription import transcribe_audio_with_whisper
from utils.Sentiment_analysis.sentiment_analysis import analyze_sentiment
from mimetypes import guess_type

UPLOAD_FOLDER = 'Uploaded_Files'
AUDIO_FOLDER = 'Audio_Files'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Enable CORS
# Enable CORS
CORS(app, resources={r"/Detect": {"origins": "https://gilded-smakager-8700a8.netlify.app"},
                     r"/progress/*": {"origins": "https://gilded-smakager-8700a8.netlify.app"}})

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
        audio_path = extract_audio(video_path)
        if not audio_path:
            return "N/A", "N/A", "No audio available"
        transcribed_text = transcribe_audio_with_whisper(audio_path)
        if not transcribed_text:
            return "N/A", "N/A", "Transcription error"
        sentiment, sentiment_score = analyze_sentiment(transcribed_text)
        return sentiment, sentiment_score, transcribed_text
    except Exception as e:
        return "N/A", "N/A", "Sentiment analysis error"

@app.route('/Detect', methods=['POST'])
def DetectPage():
    if 'media' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    media = request.files['media']
    media_filename = secure_filename(media.filename)
    media_path = os.path.join(app.config['UPLOAD_FOLDER'], media_filename)
    media.save(media_path)

    if not os.path.exists(media_path):
        return jsonify({'error': 'File upload failed'}), 500

    # Determine file type
    mime_type, _ = guess_type(media_path)
    if mime_type and mime_type.startswith('video'):
        # Video processing
        try:
            prediction = detect_fake_video(media_path)
            is_fake = prediction[0] == 0
            output = "FAKE" if is_fake else "REAL"
            confidence = prediction[1]

            # Perform sentiment analysis for videos
            sentiment, sentiment_score, transcribed_text = analyze_video_sentiment(media_path)
            emotion_analysis_result = {
                'emotion': sentiment,
                'score': sentiment_score,
                'transcribed_text': transcribed_text
            }
            response = {
                'media_type': 'video',
                'deepfake_result': {
                    'result': output,
                    'confidence': confidence
                },
                'emotion_result': emotion_analysis_result
            }
        except Exception as e:
            return jsonify({'error': 'Error during video detection'}), 500
    elif mime_type and mime_type.startswith('image'):
        # Image processing
        try:
            prediction = detect_fake_image(media_path)
            is_fake = prediction[0] == 0
            output = "FAKE" if is_fake else "REAL"
            confidence = prediction[1]
            response = {
                'media_type': 'image',
                'deepfake_result': {
                    'result': output,
                    'confidence': confidence
                }
            }
        except Exception as e:
            return jsonify({'error': 'Error during image detection'}), 500
    else:
        return jsonify({'error': 'Unsupported media type'}), 400

    # Cleanup
    if os.path.exists(media_path):
        try:
            os.remove(media_path)
        except PermissionError as e:
            time.sleep(1)
            os.remove(media_path)

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(port=5000)
