
from controller import Robot
import numpy as np
import math
import keyboard
import random


# Funciones Desarrolladas en este trabajo
import Rot_Control
import Explorar
import Condiciones_Giro
import Odometria
import Graficas

class Slave(Robot):
    # get the time step of the current world.
    timestep = 3
    
    # Especificaciones del mundo
    size_x = 5 #mt
    size_y = 5 #mt

    #------------------ Características del robot ------------------
    wheelRadius = 0.035 #radio en m 
    distanceCenter = 0.0748664*2 #0.075 #m 
    angulo = 90  # ángulo respecto marco de referencia entorno
    
    #--------------------------------------------------------------- 
    
    
    #-------------------------- Odometría -------------------------- 

    PS_Right_Anterior = 0  # Pocisión de rueda derecha en n-1
    PS_Left_Anterior  = 0  # Pocisión de rueda izquierda en n-1

    phi = angulo # rotz estimado respecto marco de referencia entorno

    # posición centroide vehículo
    xc = [0]
    yc = [0]

    # Distancia en tramos de linea recta
    Distancias_lineaRecta = []
    Angulos = []
    Distancia_Total = 0
    T_Exploracion_x = [0]
    T_Exploracion_y = [0]
    T_Exploracion_GPS_x = []
    T_Exploracion_GPS_y = []
    error_GPS_Estimado = []
    #---------------------------------------------------------------  

    #--------------------- Definiciones previas --------------------
    distanceSensors = []
    #---------------------------------------------------------------  


    def __init__(self):
        super(Slave, self).__init__()
        # Habilitar Motores
        self.left_motor = self.getDevice('motor_1')
        self.right_motor = self.getDevice('motor_2')
        
        self.left_motor.setPosition(float('inf'))
        self.left_motor.setVelocity(0.0)
        

        self.right_motor.setPosition(float('inf'))
        self.right_motor.setVelocity(0.0)

        # Habilitar sensores de  position de motores
        self.PositionSensor_left = self.getDevice('PositionSensor_1')
        self.PositionSensor_left.enable(self.timestep)
        self.PositionSensor_right = self.getDevice('PositionSensor_2')
        self.PositionSensor_right.enable(self.timestep)

        # Habilitar sensores de distancia
        for dsnumber in range(0, 6):
            self.distanceSensors.append(self.getDevice('ds_' + str(dsnumber)))
            self.distanceSensors[-1].enable(self.timestep)
        
        # Habilitar compass
        self.compass = self.getDevice('compass')
        self.compass.enable(self.timestep)

        # Habilitar GPS
        self.GPS = self.getDevice('gps')
        self.GPS.enable(self.timestep)

    
    def DatosSensores_Init(self):
        self.PS_Right_StartValue =  self.PositionSensor_right.getValue()  # PS_Right_value --> position sensor right value
        self.PS_Left_StartValue  =  self.PositionSensor_left.getValue()  # PS_Right_value --> position sensor right value

        # Offset para valores GPS 
        # Actualizar valores de GPS
        self.GPS_values = self.GPS.getValues()
        self.T_Exploracion_GPS_x.append(self.GPS_values[0]+self.size_x/2)
        self.T_Exploracion_GPS_y.append(self.GPS_values[1]+self.size_y/2)

        self.delta_GPS_Estimado_x = abs(self.T_Exploracion_GPS_x[0])
        self.delta_GPS_Estimado_y = abs(self.T_Exploracion_GPS_y[0])


    def DatosSensores(self):
        # Actualizar sensores de distancia
        self.ds0_value = self.distanceSensors[0].getValue()
        self.ds1_value = self.distanceSensors[1].getValue()
        self.ds2_value = self.distanceSensors[2].getValue()
        self.ds3_value = self.distanceSensors[3].getValue()
        self.ds4_value = self.distanceSensors[4].getValue()
        self.ds5_value = self.distanceSensors[5].getValue()

        # Actualizar sensor de compass y angulo de rotz
        self.compass_values = self.compass.getValues()
        radian = np.arctan2(self.compass_values[0],self.compass_values[1])
        self.rotz_g = radian*180/np.pi     # Rotación en el eje z del vehículo en grados
        self.rotz = radian                 # Rotación en el eje z del vehículo en radianes

        # Actualizar valores de sensores de posición de las ruedas
        self.PS_Right_value = self.PositionSensor_right.getValue()- self.PS_Right_StartValue   # PS_Right_value --> position sensor right value
        self.PS_Left_value  = self.PositionSensor_left.getValue()- self.PS_Left_StartValue    # PS_Left_value --> position sensor left value 
        
        # Actualizar valores de GPS
        self.GPS_values = self.GPS.getValues()
        

Agente_1 = Slave()

if Agente_1.step(Agente_1.timestep) != -1:
    None

Agente_1.DatosSensores_Init() 
Odometria.Odometria_Init(Agente_1)

i = False
while Agente_1.step(Agente_1.timestep) != -1:
    Agente_1.DatosSensores()
    Rot_Control.Rot_Control(Agente_1.angulo,Agente_1)
    Explorar.Explorar(Agente_1)
    

    if Agente_1.getTime() >= 40*60:
        Graficas.Trayectoria_Exploracion(Agente_1)
        Graficas.Error(Agente_1)
        
        print(Agente_1.xc[-1], "  -  ", Agente_1.T_Exploracion_x[-1], "  -  ", Agente_1.T_Exploracion_GPS_x[-1]-Agente_1.delta_GPS_Estimado_x)
        #print("tiempo al corte: ", Agente_1.getTime()," s")
        #print("Estimado: ", round(Agente_1.phi,0), " - Real: ",Agente_1.angulo)
        
        #print("cant nodos: Distancia linea: ", len(Agente_1.Distancias_lineaRecta), " - ", len(Agente_1.Angulos))
        #print("T GPS: ", len(Agente_1.T_Exploracion_GPS_x), " - ", len(Agente_1.T_Exploracion_GPS_y))
        #print("T Estimada: ", len(Agente_1.T_Exploracion_x), " - ", len(Agente_1.T_Exploracion_y))
        break

    Condiciones_Giro.DecisionGiro(Agente_1)

    if Agente_1.step(Agente_1.timestep) == -1:
        break
    



