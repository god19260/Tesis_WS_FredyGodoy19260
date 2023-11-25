#include <Wire.h>
#include <VL53L0X.h>

VL53L0X sensor;

void setup() {
  Serial.begin(115200);

  Wire.begin();
  sensor.init();
  sensor.setTimeout(500);

  // Inicializar el sensor de distancia
  if (!sensor.init()) {
    Serial.println("Failed to detect and initialize sensor!");
    while (1);
  }

  // Establecer la distancia máxima de medición en 120 cm
  sensor.setSignalRateLimit(0.5);
  sensor.setMeasurementTimingBudget(5000);
}

void loop() {
  // Realizar una medición
  Serial.print("Distance: ");
  Serial.print(sensor.readRangeSingleMillimeters());
  Serial.println(" mm");

  delay(500);  // Esperar medio segundo entre las lecturas
}