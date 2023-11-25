import serial
import time

import serial.tools.list_ports

def find_port_by_device_name(device_name):
    ports = serial.tools.list_ports.comports()
    
    for port, desc, hwid in sorted(ports):
        if device_name.lower() in desc.lower():
            return port

    return None


device_name = input("Ingrese el nombre del dispositivo para encontrar el puerto: ")

port = find_port_by_device_name(device_name)

if port:
    print(f"\nEl puerto del dispositivo '{device_name}' es: {port}")
else:
    print(f"No se encontró el dispositivo '{device_name}'.")


