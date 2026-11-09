
import os
import joblib
import pandas as pd

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score


# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "datasets" / "disaster_reports.csv"

MODEL_DIR = BASE_DIR / "ml_models" / "saved"

MODEL_PATH = MODEL_DIR / "incident_classifier.joblib"


def train_model():

    print("\n====================================")
    print(" DISASTER INCIDENT CLASSIFIER")
    print("====================================\n")

    # Load synthetic dataset
    data = pd.read_csv(DATASET_PATH)

    # Validate dataset
    if data.empty:
        raise ValueError("Dataset is empty.")

    data = data.dropna(
        subset=["description", "incident_type"]
    )

    data["description"] = data["description"].astype(str).str.strip()
    data["incident_type"] = data["incident_type"].astype(str).str.strip()

    if data["description"].eq("").any():
        raise ValueError("Dataset contains empty descriptions.")

    if data["incident_type"].nunique() < 2:
        raise ValueError("At least two incident categories are required.")

    print("Total reports:", len(data))

    print("\nCategory distribution:")
    print(data["incident_type"].value_counts())

    # Input and target
    X = data["description"]
    y = data["incident_type"]

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    # Create ML pipeline
    model = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 2),
                stop_words="english",
                max_features=5000
            )
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced"
            )
        )
    ])

    # Train model
    print("\nTraining classifier...")

    model.fit(X_train, y_train)

    # Evaluate
    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print("\n====================================")
    print(" MODEL EVALUATION")
    print("====================================")

    print(f"\nAccuracy: {accuracy * 100:.2f}%")

    print("\nClassification report:")

    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    # Create model directory
    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save trained model and metadata
    joblib.dump(
        {
            "model": model,
            "categories": sorted(y.unique()),
            "accuracy": accuracy,
            "dataset_size": len(data)
        },
        MODEL_PATH
    )

    print("\n====================================")
    print(" TRAINING COMPLETED")
    print("====================================")

    print("Model saved at:")
    print(MODEL_PATH)


if __name__ == "__main__":
    train_model()
