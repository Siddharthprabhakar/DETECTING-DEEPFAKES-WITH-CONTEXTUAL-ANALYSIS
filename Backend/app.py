from flask import Flask, request, jsonify, Response, stream_with_context
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import time
from utils.deepfake_video import detect_fake_video
from utils.sentiment_analysis import analyze_video_sentiment  # Import the emotion analysis module

UPLOAD_FOLDER = 'Uploaded_Files'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Enable CORS for /Detect and /progress endpoints
CORS(app, resources={r"/Detect": {"origins": "http://localhost:3000"}, r"/progress/*": {"origins": "http://localhost:3000"}})

# Streaming progress function
def stream_progress(video_path):
    total_steps = 100  # Simulating process taking 100 steps
    for i in range(total_steps):
        time.sleep(0.1)
        progress = i + 1
        estimated_time_left = (total_steps - progress) * 0.1
        yield f"data: {progress},{estimated_time_left}\n\n"

@app.route('/progress/<filename>', methods=['GET'])
def progress(filename):
    video_path = f"Uploaded_Files/{filename}"
    return Response(stream_with_context(stream_progress(video_path)), mimetype='text/event-stream')

@app.route('/Detect', methods=['POST'])
def DetectPage():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file uploaded'}), 400

    video = request.files['video']
    video_filename = secure_filename(video.filename)
    video.save(os.path.join(app.config['UPLOAD_FOLDER'], video_filename))
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)

    try:
        # Step 1: Detect deepfake
        prediction = detect_fake_video(video_path)
        is_fake = prediction[0] == 0  # Fake if 0, real if 1
        output = "FAKE" if is_fake else "REAL"
        confidence = prediction[1]

        # Step 2: Analyze Emotion if Real and Audio is Available
        emotion_analysis_result = None
        if not is_fake:
            # Extract audio and analyze emotion
            emotion, score, transcribed_text = analyze_video_sentiment(video_path)
            if emotion is None:
                emotion_analysis_result = {'error': 'No audio available for sentiment analysis'}
            else:
                emotion_analysis_result = {
                    'emotion': emotion,
                    'score': score,
                    'transcribed_text': transcribed_text
                }
        else:
            # For deepfakes, return a default message for emotion analysis
            emotion_analysis_result = {'emotion': 'N/A', 'score': 'N/A', 'transcribed_text': 'N/A'}

        os.remove(video_path)  # Clean up the uploaded video file

        response = {
            'deepfake_result': {
                'result': output,
                'confidence': confidence
            },
            'emotion_result': emotion_analysis_result if emotion_analysis_result else {'error': 'Emotion result not found'}
        }

        print("Response to frontend:", response)
        return jsonify(response), 200

    except Exception as e:
        print(f"Error during detection: {str(e)}")
        return jsonify({'error': 'Error during detection'}), 500

if __name__ == '__main__':
    app.run(port=5000)
