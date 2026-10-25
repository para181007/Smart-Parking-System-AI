from pathlib import Path
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "cleaned_parking_data.csv"
MODEL_DIR = ROOT / "models"
REPORT_DIR = ROOT / "reports"
MODEL_PATH = MODEL_DIR / "parking_model.pkl"

def main():
    if not DATA.exists():
        raise FileNotFoundError("Run 'py preprocess.py' first.")

    df = pd.read_csv(DATA)
    required = ["distance_cm", "hour", "slot_status"]
    if not all(c in df.columns for c in required):
        raise ValueError(f"Dataset must contain columns: {required}")
    if df["slot_status"].nunique() < 2:
        raise ValueError("Training needs both Occupied and Vacant examples.")

    X = df[["distance_cm", "hour"]]
    y = df["slot_status"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=150, max_depth=6, random_state=42, class_weight="balanced"
    )
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions, zero_division=0)
    matrix = confusion_matrix(y_test, predictions, labels=["Occupied", "Vacant"])

    MODEL_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)
    with MODEL_PATH.open("wb") as f:
        pickle.dump(model, f)

    metrics_path = REPORT_DIR / "model_metrics.txt"
    with metrics_path.open("w", encoding="utf-8") as f:
        f.write("DEMO MODEL EVALUATION\n")
        f.write(f"Test accuracy: {accuracy:.3f}\n\n")
        f.write("Classification report:\n")
        f.write(report + "\n")
        f.write("Confusion matrix (rows=true, columns=predicted; labels Occupied, Vacant):\n")
        f.write(str(matrix) + "\n")

    print(f"Model saved to: {MODEL_PATH}")
    print(f"Test accuracy: {accuracy:.3f}")
    print("\nClassification report:\n", report)
    print(f"Metrics saved to: {metrics_path}")
    print("\nNote: these metrics use synthetic demo data and are not evidence of real-world accuracy.")

if __name__ == "__main__":
    main()
