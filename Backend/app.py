from flask import Flask, request, jsonify, Response, stream_with_context
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import torch
from torch import nn
from torchvision import models, transforms
import face_recognition
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense
import time

UPLOAD_FOLDER = 'Uploaded_Files'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Enable CORS for both /Detect and /progress endpoints
CORS(app, resources={r"/Detect": {"origins": "http://localhost:3000"}, r"/progress/*": {"origins": "http://localhost:3000"}})

# Load the model without compiling it
emotion_model = tf.keras.models.load_model('model/sentiment analysis/multimodal.h5', custom_objects={'LSTM': LSTM, 'Dense': Dense}, compile=False)

# Recompile the model with updated optimizer arguments
optimizer = tf.keras.optimizers.Adadelta(learning_rate=1.0)
emotion_model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# Define the deepfake detection model architecture
class Model(nn.Module):
    def __init__(self, num_classes, latent_dim=2048, lstm_layers=1, hidden_dim=2048, bidirectional=False):
        super(Model, self).__init__()
        model = models.resnext50_32x4d(pretrained=True)
        self.model = nn.Sequential(*list(model.children())[:-2])
        self.lstm = nn.LSTM(latent_dim, hidden_dim, lstm_layers, bidirectional)
        self.relu = nn.LeakyReLU()
        self.dp = nn.Dropout(0.4)
        self.linear1 = nn.Linear(2048, num_classes)
        self.avgpool = nn.AdaptiveAvgPool2d(1)

    def forward(self, x):
        batch_size, seq_length, c, h, w = x.shape
        x = x.view(batch_size * seq_length, c, h, w)
        fmap = self.model(x)
        x = self.avgpool(fmap)
        x = x.view(batch_size, seq_length, 2048)
        x_lstm, _ = self.lstm(x, None)
        return fmap, self.dp(self.linear1(x_lstm[:, -1, :]))

def predict(model, img):
    fmap, logits = model(img)
    sm = nn.Softmax(dim=1)
    logits = sm(logits)
    _, prediction = torch.max(logits, 1)
    confidence = logits[:, int(prediction.item())].item() * 100
    return [int(prediction.item()), confidence]

class validation_dataset(torch.utils.data.Dataset):
    def __init__(self, video_names, sequence_length=60, transform=None):
        self.video_names = video_names
        self.transform = transform
        self.count = sequence_length

    def __len__(self):
        return len(self.video_names)

    def __getitem__(self, idx):
        video_path = self.video_names[idx]
        frames = []
        for i, frame in enumerate(self.frame_extract(video_path)):
            faces = face_recognition.face_locations(frame)
            try:
                top, right, bottom, left = faces[0]
                frame = frame[top:bottom, left:right, :]
            except:
                pass
            frames.append(self.transform(frame))
            if len(frames) == self.count:
                break
        frames = torch.stack(frames)
        frames = frames[:self.count]
        return frames.unsqueeze(0)

    def frame_extract(self, path):
        vidObj = cv2.VideoCapture(path)
        success = True
        while success:
            success, image = vidObj.read()
            if success:
                yield image

def detectFakeVideo(videoPath):
    im_size = 112
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]

    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((im_size, im_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean, std)
    ])

    video_dataset = validation_dataset([videoPath], sequence_length=20, transform=transform)
    model = Model(2)
    model.load_state_dict(torch.load('model/video/df_model.pt', map_location=torch.device('cpu')))
    model.eval()

    for i in range(len([videoPath])):
        prediction = predict(model, video_dataset[i])
        return prediction

def detectEmotionOnFrame(frame):
    resized_frame = cv2.resize(frame, (48, 48))
    gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
    gray_frame = np.expand_dims(gray_frame, axis=-1)
    gray_frame = np.expand_dims(gray_frame, axis=0)
    gray_frame = gray_frame / 255.0
    emotion_prediction = emotion_model.predict(gray_frame)
    return np.argmax(emotion_prediction), np.max(emotion_prediction)

def stream_progress(video_path):
    total_steps = 100  # Simulating the process taking 100 steps
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
        prediction = detectFakeVideo(video_path)

        os.remove(video_path)

        if prediction[0] == 0:
            output = "FAKE"
        else:
            output = "REAL"

        confidence = prediction[1]

        # Extract frames from video and detect emotions
        emotions_detected = []
        vidObj = cv2.VideoCapture(video_path)
        success, frame = vidObj.read()
        while success:
            faces = face_recognition.face_locations(frame)
            for (top, right, bottom, left) in faces:
                face_frame = frame[top:bottom, left:right]
                emotion, confidence = detectEmotionOnFrame(face_frame)
                emotions_detected.append({"emotion": int(emotion), "confidence": confidence})
            success, frame = vidObj.read()

        response = {
            'result': output,
            'confidence': confidence,
            'emotions': emotions_detected
        }

        return jsonify(response), 200

    except Exception as e:
        print(f"Error during detection: {str(e)}")
        return jsonify({'error': 'Error during detection'}), 500

if __name__ == '__main__':
    app.run(port=5000)
