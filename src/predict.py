
import json
import numpy as np
import tensorflow as tf

from pathlib import Path
from PIL import Image
from tensorflow.keras.applications.vgg16 import preprocess_input

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "mango_vgg16_model.keras"
LABEL_PATH = BASE_DIR / "models" / "class_names.json"

# Load model
model = tf.keras.models.load_model(MODEL_PATH)

# Load labels
with open(LABEL_PATH, "r") as file:
    class_names = json.load(file)


def predict_disease(image: Image.Image):

    image = image.convert("RGB")
    image = image.resize((224, 224))

    image_array = np.array(image, dtype=np.float32)

    image_array = preprocess_input(image_array)
    image_array = np.expand_dims(image_array, axis=0)

    predictions = model.predict(image_array, verbose=0)

    predicted_index = np.argmax(predictions[0])
    confidence = float(predictions[0][predicted_index])

    return {
        "disease": class_names[predicted_index],
        "confidence": round(confidence * 100, 2)
    }
