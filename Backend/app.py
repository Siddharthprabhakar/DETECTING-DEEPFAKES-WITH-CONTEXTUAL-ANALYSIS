# app.py
from flask import Flask, request, jsonify, Response, stream_with_context
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import time
from utils.deepfake_video import detect_fake_video

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
        prediction = detect_fake_video(video_path)

        os.remove(video_path)

        if prediction[0] == 0:
            output = "FAKE"
        else:
            output = "REAL"

        confidence = prediction[1]

        response = {
            'result': output,
            'confidence': confidence
        }

        return jsonify(response), 200

    except Exception as e:
        print(f"Error during detection: {str(e)}")
        return jsonify({'error': 'Error during detection'}), 500

if __name__ == '__main__':
    app.run(port=5000)
