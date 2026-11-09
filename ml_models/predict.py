
from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "ml_models" / "saved" / "incident_classifier.joblib"

# Load the trained model once when this module is imported.
if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Trained model not found: {MODEL_PATH}. "
        "Run python ml_models/train_classifier.py first."
    )

saved_data = joblib.load(MODEL_PATH)
model = saved_data["model"]
categories = saved_data["categories"]


def predict_incident(description):
    """
    Predict the likely incident category from a report description.

    Returns a prediction and model score. The score is not a
    calibrated measure of real-world certainty.
    """
    description = description.strip()

    if not description:
        raise ValueError("Incident description cannot be empty.")

    probabilities = model.predict_proba([description])[0]
    predicted_index = probabilities.argmax()

    predicted_type = model.classes_[predicted_index]
    model_score = float(probabilities[predicted_index])

    return {
        "predicted_type": predicted_type,
        "model_score": model_score,
        "categories": categories,
    }
