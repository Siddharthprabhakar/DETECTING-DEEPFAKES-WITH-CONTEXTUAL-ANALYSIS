import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img

# Load the MobileNet model for deepfake detection
model_path = 'models/image/mobilenet_deepfake.h5'
model = load_model(model_path)

# Define image preprocessing function
def preprocess_image(image_path, target_size=(224, 224)):
    # Load image and resize to the target size
    image = load_img(image_path, target_size=target_size)
    # Convert the image to an array and add a batch dimension
    image_array = img_to_array(image)
    image_array = np.expand_dims(image_array, axis=0)
    # Scale pixel values to the range [0, 1]
    image_array /= 255.0
    return image_array

# Define the main prediction function for images
def detect_fake_image(image_path):
    # Preprocess the image
    processed_image = preprocess_image(image_path)
    # Get prediction
    prediction = model.predict(processed_image)
    probability_fake = prediction[0][0]  # Model output: probability of being a fake
    
    # Log the prediction confidence
    print(f"Model prediction probability for fake: {probability_fake}")

    # Determine if the image is classified as fake or real based on threshold
    is_fake = probability_fake > 0.5  # Adjust threshold if needed
    label = "FAKE" if is_fake else "REAL"
    confidence = probability_fake * 100 if is_fake else (1 - probability_fake) * 100
    return label, confidence
