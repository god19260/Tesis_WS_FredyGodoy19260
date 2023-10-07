
from controller import Robot
import numpy as np
import math
import matplotlib.pyplot as plt
import keyboard
import random
import Gen_Trayectoria

class Slave(Robot):
    # get the time step of the current world.
    timestep = 3

    # Caracteristicas del robot
    maxSpeed = 0.035 #mt/s
    wheelRadius = 0.035 #radio en m 
    distanceCenter = 0.075 #m
    rev = maxSpeed/(2*3.14*wheelRadius)*60
    
    # Definiciones previas
    distanceSensors = []



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

    def run(self):
               

        while self.step(self.timestep) != -1:
            if self.step(self.timestep) == -1:
                break
                 
    def DatosSensores(self):
        # Actualizar sensores de distancia
        self.ds0_value = self.distanceSensors[0].getValue()
        self.ds1_value = self.distanceSensors[1].getValue()
        self.ds2_value = self.distanceSensors[2].getValue()
        self.ds3_value = self.distanceSensors[3].getValue()
        self.ds4_value = self.distanceSensors[4].getValue()
        self.ds5_value = self.distanceSensors[5].getValue()

        # Actualizar sensor de compass y angulo de rotación en z
        self.compass_values = self.compass.getValues()
        radian = np.arctan2(self.compass_values[0],self.compass_values[1])
        self.rotz_g = radian*180/np.pi
        self.rotz = radian

        # Actualizar valores de sensores de posición de las ruedas
        self.PS_Right_value = round(self.PositionSensor_right.getValue() - self.PS_Right_StartValue, 4)  # PS_Right_value --> position sensor right value
        self.PS_Left_value = round(self.PositionSensor_left.getValue() - self.PS_Left_StartValue,4)    # PS_Left_value --> position sensor left value 
        
        self.revsRight = self.PS_Right_value/(2*np.pi)
        self.revsLeft = self.PS_Left_value/(2*np.pi)
        
        self.DRW_Right = round(self.revsRight*2*np.pi*self.wheelRadius,10)    # Distancia recorrida por la llanta derecha
        self.DRW_Left = round(self.revsLeft*2*np.pi*self.wheelRadius,10)      # Distancia recorrida por la llanta izquierda

        # Actualizar valores de GPS
        self.GPS_values = self.GPS.getValues()


controller = Slave()
controller.run()

