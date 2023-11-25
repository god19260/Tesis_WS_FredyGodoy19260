#include <BluetoothSerial.h>
#include <cstdio>
#include <ESP32Servo.h>
#include <Wire.h>
#include <VL53L0X.h>


#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;
Servo miServo;
VL53L0X sensor;


#define SERVO_PIN 15  // El pin al que está conectado el servo
#define LED_Azul 26
#define LED_Verde 27
#define tiempo 1000
#define push_button 23


int mensaje;
int distancias[180/5];
int angulos[180/5];
int lectura = 0;
int iteracion = 0;

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32"); // Bluetooth device name

  pinMode(LED_Verde, OUTPUT);
  pinMode(LED_Azul, OUTPUT);
  pinMode(push_button, INPUT_PULLUP);

  digitalWrite(LED_Verde, LOW);
  digitalWrite(LED_Azul, LOW);

  miServo.attach(SERVO_PIN);  // Asocia el objeto Servo al pin especificado
  

  Wire.begin();
  sensor.init();
  sensor.setTimeout(500);

  // Inicializar el sensor de distancia
  if (!sensor.init()) {
    Serial.println("Failed to detect and initialize sensor!");
    //while (1);
  }
  // Establecer la distancia máxima de medición en 120 cm
  sensor.setSignalRateLimit(0.1);
  sensor.setMeasurementTimingBudget(50000);
  Serial.print("Primera lectura: ");
  Serial.println(sensor.readRangeSingleMillimeters());


  // Rutina de leds iniciales
  init_blink();
  miServo.write(90);

}

void loop() {
  //int datos[] = {0,1,2,3,4,5,6,7};
  //char charvariable[20]; // Make sure the buffer is large enough
  //sprintf(charvariable, "%", datos);
  //Serial.println(charvariable);
  digitalWrite(LED_Azul,HIGH);
  if (!digitalRead(push_button)){
    digitalWrite(LED_Azul,LOW);
    Rutina();
  }
  
  if (SerialBT.available()) {
    mensaje = SerialBT.read();
    Serial.println("Received data: " + mensaje);

    // Send a response back
    SerialBT.println("HOLAA"); // Move to the next line after printing the array

    send_blink();
  }
  //send_blink();
  // Your other code can go here
  delay(20); // Delay for a while to avoid spamming the Bluetooth connection
}


// Funciones 
void send_blink(){
  digitalWrite(LED_Azul,HIGH);
  delay(100);
  digitalWrite(LED_Azul,LOW);
  delay(300);

  digitalWrite(LED_Azul,HIGH);
  delay(100);
  digitalWrite(LED_Azul,LOW);
  delay(300);
}

void init_blink(){
  for (int i = 0;i<=2;i++){
    digitalWrite(LED_Azul,HIGH);
    delay(50);
    digitalWrite(LED_Azul,LOW);
    delay(100);

    digitalWrite(LED_Verde,HIGH);
    delay(50);
    digitalWrite(LED_Verde,LOW);
    delay(100);
  }
}

void finish_task_blink(){
  for (int i = 0;i<=2;i++){
    digitalWrite(LED_Azul,HIGH);
    delay(100);
    digitalWrite(LED_Azul,LOW);
    delay(100);
  }
  digitalWrite(LED_Verde,HIGH);
}

void Rutina(){
  //memset(distancias, 0, sizeof(distancias));
  //memset(angulos, 0, sizeof(angulos));
  iteracion = 0;

  int angulo = 90;
  miServo.write(angulo);
  delay(tiempo);

  for (angulo = 90-45; angulo<=90+45;angulo=angulo+5 ){
    angulos[iteracion] = angulo;
    miServo.write(angulo);
    delay(tiempo/5);
    lectura_vl53x0();
    iteracion = iteracion+1;
  }

  for (; angulo>=90-45;angulo=angulo-5 ){
    angulos[iteracion] = angulo;
    miServo.write(angulo);
    delay(tiempo/5);
    lectura_vl53x0();
    iteracion = iteracion+1;
  }

  finish_task_blink();
  miServo.write(90);
  Serial.print("Angulos: ");
  Serial.print("[");
  for(int i = 0; i < sizeof(angulos); i++){
    Serial.print(angulos[i]);
    Serial.print(",");
  }
  Serial.println("]");

  Serial.print("Distancias: ");
  Serial.print("[");
  for(int i = 0; i < sizeof(distancias); i++){
    Serial.print(distancias[i]);
    Serial.print(",");
  }
  Serial.print("]");

}

void lectura_vl53x0(){
  // Realizar una medición
  lectura = sensor.readRangeSingleMillimeters();
  distancias[iteracion] = lectura;
  //Serial.print("Distance: ");
  Serial.print(lectura);
  Serial.print(",");
  //Serial.println(" mm");
  delay(10);
}
