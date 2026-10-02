import json
import numpy as np
import tensorflow as tf
from PIL import Image

model = tf.keras.models.load_model("ml/model/cropcare_model.keras")
class_names = json.load(open("ml/model/class_names.json"))

print("Model loaded")
print("Number of classes:", len(class_names))
print("First class:", class_names[0])

def predict_image(path):
    img = Image.open(path).convert("RGB").resize((224, 224))
    arr = np.expand_dims(np.array(img), axis=0)
    probs = model.predict(arr, verbose=0)[0]

    top3_idx = np.argsort(probs)[::-1][:3]
    top3 = [
        {"name": class_names[i], "confidence": round(float(probs[i]) * 100, 1)}
        for i in top3_idx
    ]
    return {
        "disease": top3[0]["name"],
        "confidence": top3[0]["confidence"],
        "top3": top3,
    }


if __name__ == "__main__":
    result = predict_image("dataset/split/test/Potato___healthy/3c0d6888-c7e1-4cf8-9c25-9a0b8c62ba72___RS_HL 1780.JPG")
    print(result)
    