# Detecting Deepfakes With Contextual Analysis

A full-stack deepfake detection project that analyzes uploaded images and videos through a React frontend and a Flask-based machine learning backend. The backend classifies media as real or fake, and for videos it also extracts audio, transcribes speech with Whisper, and runs sentiment analysis to provide additional context around the media.

## Features

- Upload image or video files from the browser.
- Detect image deepfakes with a MobileNet/Keras model.
- Detect video deepfakes with a ResNeXt + LSTM PyTorch model.
- Extract audio from uploaded videos.
- Transcribe video audio with Whisper.
- Run text sentiment analysis with a DistilBERT sentiment model.
- Display detection result, confidence score, media type, transcription, and sentiment result.
- Stream basic processing progress from the backend to the frontend.

## Tech Stack

### Frontend

- React
- React Router
- Tailwind CSS
- DaisyUI
- Axios
- React Dropzone
- Chart.js

### Backend

- Flask
- Flask-CORS
- PyTorch and torchvision
- TensorFlow/Keras
- OpenCV
- face_recognition
- MoviePy
- Whisper
- Hugging Face Transformers

## Project Structure

```text
.
|-- Backend/
|   |-- app.py
|   |-- config.py
|   |-- requirements.txt
|   |-- models/
|   |   |-- image/
|   |   |   `-- mobilenet_deepfake.h5
|   |   |-- video/
|   |   |   `-- df_model.pt
|   |   `-- sentiment analysis/
|   `-- utils/
|       |-- deepfake_image.py
|       |-- deepfake_video.py
|       `-- Sentiment_analysis/
|-- Frontend/
|   |-- public/
|   |-- src/
|   |   |-- Component/
|   |   |-- Pages/
|   |   `-- App.js
|   `-- package.json
|-- DiagramFiles/
|-- LICENSE
`-- README.md
```

## Prerequisites

- Node.js and npm
- Python 3.9 or newer
- pip
- FFmpeg, required by MoviePy and Whisper audio processing
- Model files placed in the expected backend paths

> Note: `face_recognition` depends on `dlib`, which may require CMake and C++ build tools on Windows.

## Model Files

The backend expects these model files:

```text
Backend/models/image/mobilenet_deepfake.h5
Backend/models/video/df_model.pt
```

Large model files are ignored by `.gitignore`, so they may need to be downloaded or copied into the project manually before running detection. The image model is loaded from `Backend/utils/deepfake_image.py`; the video model is loaded from `Backend/utils/deepfake_video.py`.

## Backend Setup

From the project root:

```powershell
cd Backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

The image detector imports TensorFlow/Keras. If TensorFlow is not already available in your environment, install it as well:

```powershell
pip install tensorflow
```

Start the Flask server:

```powershell
python app.py
```

The backend runs on:

```text
http://localhost:5000
```

## Frontend Setup

Open a second terminal from the project root:

```powershell
cd Frontend
npm install
npm start
```

The React app runs on:

```text
http://localhost:3000
```

## Local CORS Note

`Backend/app.py` currently configures CORS for the deployed Netlify frontend. For local frontend testing, add `http://localhost:3000` to the allowed origins for `/Detect` and `/progress/*`.

Example:

```python
CORS(app, resources={
    r"/Detect": {"origins": ["http://localhost:3000", "https://gilded-smakager-8700a8.netlify.app"]},
    r"/progress/*": {"origins": ["http://localhost:3000", "https://gilded-smakager-8700a8.netlify.app"]},
})
```

## API Endpoints

### `POST /Detect`

Uploads and analyzes an image or video file.

Request:

- Form field: `media`
- Accepted media types: image and video files

Example response for an image:

```json
{
  "media_type": "image",
  "deepfake_result": {
    "result": "REAL",
    "confidence": 91.24
  }
}
```

Example response for a video:

```json
{
  "media_type": "video",
  "deepfake_result": {
    "result": "FAKE",
    "confidence": 86.72
  },
  "emotion_result": {
    "emotion": "negative",
    "score": 0.98,
    "transcribed_text": "Transcribed speech from the uploaded video."
  }
}
```

### `GET /progress/<filename>`

Streams basic server-sent progress events for a file being processed.

## How It Works

1. The user uploads an image or video in the React interface.
2. The frontend sends the file to the Flask backend using `multipart/form-data`.
3. The backend identifies the uploaded media type.
4. Images are processed by the MobileNet/Keras image detector.
5. Videos are processed frame-by-frame by the PyTorch video detector.
6. For videos, the backend extracts audio, transcribes it with Whisper, and analyzes sentiment.
7. The backend returns the result and confidence score to the frontend.
8. Uploaded files are removed from temporary storage after processing.

## Diagrams

PlantUML diagrams are available in the `DiagramFiles/` directory, including activity and block diagrams for the system workflow.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
