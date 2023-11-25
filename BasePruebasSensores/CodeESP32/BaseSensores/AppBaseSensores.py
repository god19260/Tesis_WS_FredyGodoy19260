import serial
import time

import serial.tools.list_ports



# Replace "COMx" with the actual COM port of your ESP32 Bluetooth device
try:
    serial_port = serial.Serial('COM12', 9600, timeout=1)
except:
    print("No se logro conexión")

    
def send_data(data):
    serial_port.write(data.encode())
    print(f"Sent data: {data}")
        

def read_data():
    mensaje = serial_port.read_until('\n')
    print(f"-- MENSAJE RECIBIDO: {mensaje.decode('utf-8')}")




try:
    while True:
        message = input("\nEnter a message to send: ")
        send_data(message)
        read_data()
        

        time.sleep(1)  # Delay to avoid sending data too quickly
except KeyboardInterrupt:
    print("Exiting program.")
    serial_port.close()

