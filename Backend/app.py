from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import torch
from torch import nn
from torchvision import models, transforms
import face_recognition
import numpy as np
import cv2

UPLOAD_FOLDER = 'Uploaded_Files'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app, resources={r"/Detect": {"origins": "http://localhost:3000"}})


# Define the model architecture
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


# Helper functions and dataset classes
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
    model.load_state_dict(torch.load('model/df_model.pt', map_location=torch.device('cpu')))
    model.eval()

    for i in range(len([videoPath])):
        prediction = predict(model, video_dataset[i])
        return prediction


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
        response = {
            'result': output,  # Changed 'output' to 'result' to match frontend
            'confidence': confidence
        }

        return jsonify(response), 200

    except Exception as e:
        print(f"Error during detection: {str(e)}")
        return jsonify({'error': 'Error during detection'}), 500


if __name__ == '__main__':
    app.run(port=5000)
