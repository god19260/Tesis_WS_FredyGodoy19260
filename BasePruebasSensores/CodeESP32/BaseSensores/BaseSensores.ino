#include <Wire.h>
#include <Adafruit_VL53L0X.h>
#include <ESP32Servo.h>

Adafruit_VL53L0X lox = Adafruit_VL53L0X();
Servo miServo;

#define SERVO_PIN 15  // El pin al que está conectado el servo
#define LED_Azul 26
#define LED_Verde 27
#define tiempo 100
#define push_button 23

void setup() {
  Serial.begin(115200);
  Wire.begin();

  if (!lox.begin()) {
    Serial.println(F("Failed to boot VL53L0X"));
    while (1);
  }

  Serial.println(F("VL53L0X Ready!"));

  pinMode(LED_Verde, OUTPUT);
  pinMode(LED_Azul, OUTPUT);
  pinMode(push_button, INPUT_PULLUP);

  digitalWrite(LED_Verde, LOW);
  digitalWrite(LED_Azul, LOW);

  miServo.attach(SERVO_PIN);  // Asocia el objeto Servo al pin especificado
}

void loop() {
  // Control del servo
  miServo.write(0);
  delay(tiempo);

  miServo.write(90);
  delay(tiempo);

  miServo.write(180);
  delay(tiempo);

  // Medición con el sensor VL53L0X
  VL53L0X_RangingMeasurementData_t measure;
  lox.rangingTest(&measure, false);

  if (measure.RangeStatus != 4) {  // 4 significa que no hay error
    Serial.print(F("Distancia (mm): "));
    Serial.println(measure.RangeMilliMeter);
  } else {
    Serial.println(F("Fuera de rango"));
  }

  // Parpadeo de LEDs en respuesta a un botón
  if (digitalRead(push_button)) {
    digitalWrite(LED_Azul, HIGH);
    delay(tiempo);
    digitalWrite(LED_Azul, LOW);
    delay(tiempo);

    digitalWrite(LED_Verde, HIGH);
    delay(tiempo);
    digitalWrite(LED_Verde, LOW);
    delay(tiempo);
  } else {
    while (!digitalRead(push_button)) {
      digitalWrite(LED_Azul, HIGH);
    }
    digitalWrite(LED_Azul, LOW);
  }
}
