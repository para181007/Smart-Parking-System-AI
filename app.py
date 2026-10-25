from pathlib import Path
import pickle
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "cleaned_parking_data.csv"
MODEL_PATH = ROOT / "models" / "parking_model.pkl"

st.set_page_config(page_title="Smart Parking AI", page_icon="🚗", layout="wide")
st.title("🚗 Smart Parking System Using AI")
st.caption("Beginner prototype: sample-data dashboard + ML occupancy prediction")

if not DATA_PATH.exists() or not MODEL_PATH.exists():
    st.warning("Project files are not ready yet. Run the setup commands in README.md first.")
    st.code("py -m pip install -r requirements.txt\npy preprocess.py\npy eda.py\npy train_model.py\npy -m streamlit run app.py", language="powershell")
    st.stop()

df = pd.read_csv(DATA_PATH)
with MODEL_PATH.open("rb") as f:
    model = pickle.load(f)

st.info(
    "This version uses synthetic sample data. It does not show live hardware readings. "
    "Connect and record your own sensor readings before presenting it as a real-time system."
)

col1, col2, col3 = st.columns(3)
total = len(df)
occupied = int((df["slot_status"] == "Occupied").sum())
vacant = int((df["slot_status"] == "Vacant").sum())
col1.metric("Total readings", total)
col2.metric("Occupied readings", occupied)
col3.metric("Vacant readings", vacant)

left, right = st.columns(2)
with left:
    st.subheader("Occupancy distribution")
    status_counts = df["slot_status"].value_counts().reindex(["Occupied", "Vacant"], fill_value=0)
    st.bar_chart(status_counts)
with right:
    st.subheader("Distance by status")
    distance_summary = df.groupby("slot_status")["distance_cm"].mean().reindex(["Occupied", "Vacant"])
    st.bar_chart(distance_summary)

st.subheader("Sample data")
st.dataframe(df.tail(20), use_container_width=True)

st.divider()
st.subheader("Try a parking prediction")
st.write("Enter a sample sensor distance. The model uses distance and hour to predict status.")
c1, c2 = st.columns(2)
with c1:
    distance = st.slider("Measured distance (cm)", min_value=2.0, max_value=150.0, value=15.0, step=1.0)
with c2:
    hour = st.slider("Hour of day", min_value=0, max_value=23, value=10, step=1)

if st.button("Predict parking status", type="primary"):
    result = model.predict(pd.DataFrame([{"distance_cm": distance, "hour": hour}]))[0]
    if result == "Occupied":
        st.warning(f"Model prediction: {result}")
    else:
        st.success(f"Model prediction: {result}")
    st.caption("Demonstration prediction only; calibrate and validate using your own labelled sensor data.")
