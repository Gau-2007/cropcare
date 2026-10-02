import sys
import uuid
from pathlib import Path
from flask import Flask, request, jsonify

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from ml.predict import predict_image
from db import get_disease_info, save_prediction, get_history
from weather import get_forecast
from risk import assess_risk

UPLOADS = ROOT / "uploads"
UPLOADS.mkdir(exist_ok=True)
ALLOWED = {".jpg", ".jpeg", ".png"}
DEFAULT_LAT, DEFAULT_LON = 18.63, 73.80   # Pimpri-Chinchwad, used if location is not shared
LOW_CONFIDENCE = 60

app = Flask(__name__, static_folder=str(ROOT / "frontend"), static_url_path="")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024   # 5 MB


@app.errorhandler(413)
def too_large(e):
    return jsonify(success=False, error="Image is too large (max 5 MB)"), 413


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

    try:
        result = predict_image(save_path)
    except Exception:
        return jsonify(success=False, error="Could not read this image"), 400

    # readable names for the top 3
    for item in result["top3"]:
        info = get_disease_info(item["name"])
        item["display_name"] = info["display_name"] if info else item["name"]

    info = get_disease_info(result["disease"]) or {}

    # weather (optional; the app still works if it fails)
    try:
        lat = float(request.form.get("lat", DEFAULT_LAT))
        lon = float(request.form.get("lon", DEFAULT_LON))
    except ValueError:
        lat, lon = DEFAULT_LAT, DEFAULT_LON
    try:
        days = get_forecast(lat, lon)
    except Exception:
        days = None

    risk, water = assess_risk(result["disease"], days)
    save_prediction(save_path.name, result["disease"], result["confidence"])

    return jsonify(
        success=True,
        disease=result["disease"],
        display_name=info.get("display_name", result["disease"]),
        crop=info.get("crop", ""),
        confidence=result["confidence"],
        low_confidence=result["confidence"] < LOW_CONFIDENCE,
        is_healthy="healthy" in result["disease"],
        top3=result["top3"],
        info={k: info.get(k) for k in ("description", "symptoms", "prevention", "treatment")},
        risk=risk,
        water=water,
        weather=days,
    )


@app.route("/history")
def history_route():
    return jsonify(get_history(5))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)