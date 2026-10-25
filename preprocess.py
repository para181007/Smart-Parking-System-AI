from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "data" / "parking_data.csv"
OUTPUT = ROOT / "data" / "cleaned_parking_data.csv"
REQUIRED = ["distance_cm", "hour", "day", "slot_status"]

def main():
    if not INPUT.exists():
        raise FileNotFoundError(
            f"Could not find {INPUT}. Run 'py generate_sample_data.py' from the project folder."
        )

    df = pd.read_csv(INPUT)
    missing_columns = [col for col in REQUIRED if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {missing_columns}")

    print("Original dataset shape:", df.shape)
    print("\nMissing values before cleaning:\n", df.isna().sum())

    df = df.drop_duplicates()
    df["distance_cm"] = pd.to_numeric(df["distance_cm"], errors="coerce")
    df["hour"] = pd.to_numeric(df["hour"], errors="coerce")
    df["day"] = df["day"].astype("string").str.strip()
    df["slot_status"] = df["slot_status"].astype("string").str.strip().str.title()

    df = df.dropna(subset=REQUIRED)
    df = df[df["distance_cm"].between(0, 400)]
    df = df[df["hour"].between(0, 23)]
    df = df[df["slot_status"].isin(["Occupied", "Vacant"])]

    df["hour"] = df["hour"].astype(int)
    df["distance_cm"] = df["distance_cm"].astype(float)

    OUTPUT.parent.mkdir(exist_ok=True)
    df.to_csv(OUTPUT, index=False)

    print("\nCleaned dataset shape:", df.shape)
    print("\nMissing values after cleaning:\n", df.isna().sum())
    print(f"\nPreprocessing complete. Saved: {OUTPUT}")

if __name__ == "__main__":
    main()
