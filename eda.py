from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "cleaned_parking_data.csv"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

def main():
    if not DATA.exists():
        raise FileNotFoundError("Run 'py preprocess.py' first.")
    df = pd.read_csv(DATA)

    counts = df["slot_status"].value_counts()
    plt.figure()
    counts.reindex(["Occupied", "Vacant"], fill_value=0).plot(kind="bar")
    plt.title("Parking Occupancy Counts")
    plt.xlabel("Slot status")
    plt.ylabel("Number of readings")
    plt.tight_layout()
    plt.savefig(REPORTS / "occupancy_counts.png")
    plt.close()

    plt.figure()
    df.boxplot(column="distance_cm", by="slot_status")
    plt.title("Distance by Parking Status")
    plt.suptitle("")
    plt.xlabel("Slot status")
    plt.ylabel("Distance (cm)")
    plt.tight_layout()
    plt.savefig(REPORTS / "distance_by_status.png")
    plt.close()

    print("EDA complete. Charts saved in the reports folder.")

if __name__ == "__main__":
    main()
