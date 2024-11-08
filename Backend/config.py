import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Upload folder
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'Uploaded_Files')

# Model paths
VIDEO_DEEPFAKE_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'video', 'df_model.pt')
IMAGE_DEEPFAKE_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'image')
SENTIMENT_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'sentiment analysis')

# Replace with your Hugging Face API URL and API Key for emotion detection
HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/your-model"
HUGGING_FACE_API_KEY = "your-hugging-face-api-key"
