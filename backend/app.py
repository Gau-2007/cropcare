import sys
import uuid
from pathlib import Path
from flask import Flask, request, jsonify

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from ml.predict import predict_image

UPLOADS = ROOT / "uploads"
UPLOADS.mkdir(exist_ok=True)
ALLOWED = {".jpg", ".jpeg", ".png"}

app = Flask(__name__, static_folder=str(ROOT / "frontend"), static_url_path="")


@app.route("/")
def home():
    return app.send_static_file("index.html")


@app.route("/predict", methods=["POST"])
def predict_route():
    file = request.files.get("image")
    if file is None or file.filename == "":
        return jsonify(success=False, error="No image uploaded"), 400

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED:
        return jsonify(success=False, error="Only JPG or PNG images allowed"), 400

    save_path = UPLOADS / f"{uuid.uuid4().hex}{ext}"
    file.save(save_path)

    result = predict_image(save_path)
    return jsonify(success=True, **result)


if __name__ == "__main__":
    app.run(debug=True)