/*
  Optional ESP32 + HC-SR04 starter sketch.
  Sends a distance measurement to the Serial Monitor over USB.

  Wiring example (check your exact board):
    HC-SR04 VCC  -> 5V/VIN
    HC-SR04 GND  -> GND
    HC-SR04 TRIG -> GPIO 5
    HC-SR04 ECHO -> GPIO 18 THROUGH A VOLTAGE DIVIDER/LEVEL SHIFTER

  IMPORTANT: ESP32 GPIOs are 3.3 V logic. Do not connect a 5 V ECHO signal
  directly to an ESP32 GPIO.
*/

const int TRIG_PIN = 5;
const int ECHO_PIN = 18;
const float OCCUPIED_THRESHOLD_CM = 25.0; // Calibrate for your model.

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  digitalWrite(TRIG_PIN, LOW);
  delay(500);
  Serial.println("distance_cm,slot_status");
}

void loop() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Timeout prevents waiting indefinitely if no echo is received.
  unsigned long duration = pulseIn(ECHO_PIN, HIGH, 30000UL);

  if (duration == 0) {
    Serial.println("NO_ECHO,Unknown");
  } else {
    float distanceCm = duration * 0.0343 / 2.0;
    const char* status = (distanceCm < OCCUPIED_THRESHOLD_CM) ? "Occupied" : "Vacant";

    Serial.print(distanceCm, 2);
    Serial.print(",");
    Serial.println(status);
  }

  delay(1000);
}
