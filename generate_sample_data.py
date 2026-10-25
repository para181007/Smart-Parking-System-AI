from pathlib import Path
import csv
import random
from datetime import datetime, timedelta

random.seed(42)
ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
OUT = DATA_DIR / "parking_data.csv"

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
start = datetime(2026, 1, 5, 7, 0, 0)
rows = []

# Synthetic demo data: occupancy is correlated with distance, but includes noise.
for i in range(300):
    timestamp = start + timedelta(minutes=15 * i)
    hour = timestamp.hour
    day = days[timestamp.weekday()]
    # More busy during common work/school hours
    probability_occupied = 0.35 + (0.25 if 8 <= hour <= 10 else 0) + (0.20 if 16 <= hour <= 18 else 0)
    probability_occupied = min(probability_occupied, 0.85)
    occupied = random.random() < probability_occupied

    if occupied:
        distance = random.uniform(4, 22)
        if random.random() < 0.06:  # occasional noisy measurement
            distance = random.uniform(28, 55)
        status = "Occupied"
    else:
        distance = random.uniform(35, 100)
        if random.random() < 0.06:
            distance = random.uniform(8, 26)
        status = "Vacant"

    rows.append({
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "distance_cm": round(distance, 2),
        "hour": hour,
        "day": day,
        "slot_status": status,
    })

with OUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["timestamp", "distance_cm", "hour", "day", "slot_status"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Created {OUT} with {len(rows)} synthetic demo rows.")
