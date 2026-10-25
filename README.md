# Smart Parking System Using AI and Ultrasonic Sensors

A beginner-friendly project starter for VS Code. It includes:
- Sample parking sensor dataset
- Data preprocessing
- Exploratory data analysis (EDA) charts
- Machine-learning model training and evaluation
- Streamlit dashboard
- Optional Arduino/ESP32 HC-SR04 example sketch

## 1. Requirements
Install Python 3.10 or newer and VS Code. During Python installation on Windows, select **Add Python to PATH** if offered.

## 2. Open the project
1. Extract the ZIP file.
2. In VS Code, choose **File → Open Folder**.
3. Select the extracted `Smart_Parking_AI_Project` folder.
4. Open **Terminal → New Terminal**.

## 3. Install the libraries
On Windows, try:

```powershell
py -m pip install -r requirements.txt
```

If `py` is not recognized, try:

```powershell
python -m pip install -r requirements.txt
```

If both commands fail, install Python from https://www.python.org/downloads/ and make sure to enable **Add Python to PATH**, then restart VS Code.

## 4. Run the project in order

### A. Create sample data (optional)
A sample `data/parking_data.csv` is already included. To regenerate it:

```powershell
py generate_sample_data.py
```

### B. Preprocess the data
```powershell
py preprocess.py
```

This creates `data/cleaned_parking_data.csv`.

### C. Train and evaluate the AI model
```powershell
py train_model.py
```

This creates `models/parking_model.pkl` and `reports/model_metrics.txt`.

### D. Launch the dashboard
```powershell
py -m streamlit run app.py
```

Open the local URL shown in the terminal if the browser does not open automatically.

## 5. What the dashboard does
- Shows a sample dataset and summary statistics
- Displays occupancy charts
- Lets you enter a distance and hour to get a model prediction
- Shows a clear note that sample-data predictions are demonstrations, not live sensor readings

## 6. Sensor and hardware notes
The sketch in `arduino/esp32_hcsr04.ino` is an optional starting point for an ESP32 and HC-SR04 sensor. It sends distance readings over USB serial.

- Connect the sensor's **TRIG** and **ECHO** pins to the GPIOs defined in the sketch.
- Many ESP32 boards use 3.3 V logic. The HC-SR04 ECHO output can be 5 V, so use a suitable voltage divider/level shifter before connecting ECHO to an ESP32 GPIO.
- Check your specific board's pinout and sensor wiring before powering the circuit.
- The included Streamlit app does not automatically connect to the hardware. The sensor sketch is a separate prototype component; serial integration is a next step.

## 7. Important project limitation
The included CSV contains synthetic sample readings so you can learn the workflow. Model metrics from synthetic data do not prove real-world performance. For your final demonstration, collect labelled readings from your own sensor setup, calibrate the distance threshold for your parking slot, and retrain/evaluate the model on representative data.

## 8. Project workflow
Ultrasonic sensor → distance reading and occupancy label → CSV data collection → preprocessing → EDA → model training/evaluation → dashboard.

## Troubleshooting
- **`python` not recognized:** try `py --version`; if needed reinstall Python with **Add Python to PATH** selected and restart VS Code.
- **`No module named pandas`:** run `py -m pip install -r requirements.txt`.
- **`File not found`:** confirm VS Code opened the extracted project root folder and run commands from that folder.
