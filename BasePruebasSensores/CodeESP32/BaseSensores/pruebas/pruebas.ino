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

  Serial.println(F("Inicio"));

  pinMode(LED_Verde, OUTPUT);
  pinMode(LED_Azul, OUTPUT);
  pinMode(push_button, INPUT_PULLUP);

  digitalWrite(LED_Verde, LOW);
  digitalWrite(LED_Azul, LOW);

}

void loop() {
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
