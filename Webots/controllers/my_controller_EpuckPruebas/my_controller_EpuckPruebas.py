"""my_controller_EpuckPruebas controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor


from controller import Robot
from Funciones import bearing
import numpy as np
Robot_1 = Robot()


# get the time step of the current world.
timestep = 5
maxSpeed = 0.035 #mt/s
r = 0.035 # radio en m 
rev = maxSpeed/(2*3.14*r)*60
   
# -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# -+-+-+-+-+-+-+-+-+-+ Configuraciones +-+-+-+-+-+-+-+-+-+-+-+-

# Habilitar motores
left_motor = Robot_1.getDevice('motor_1')
right_motor = Robot_1.getDevice('motor_2')

PositionSensor_left = Robot_1.getDevice('PositionSensor_1')
PositionSensor_left.enable(timestep)
PositionSensor_right = Robot_1.getDevice('PositionSensor_2')
PositionSensor_right.enable(timestep)

left_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)

right_motor.setPosition(float('inf'))
right_motor.setVelocity(0.0)

# Habilitar Sensores de distancia
ds_0 = Robot_1.getDevice('ds_0')
ds_0.enable(timestep)

ds_1 = Robot_1.getDevice('ds_1')
ds_1.enable(timestep)

ds_2 = Robot_1.getDevice('ds_2')
ds_2.enable(timestep)

ds_3 = Robot_1.getDevice('ds_3')
ds_3.enable(timestep)

ds_4 = Robot_1.getDevice('ds_4')
ds_4.enable(timestep)

ds_5 = Robot_1.getDevice('ds_5')
ds_5.enable(timestep)

# Habilitar Compass
compass = Robot_1.getDevice('compass')
compass.enable(timestep)



# -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# -+-+-+-+-+-+-+-+-+-+- Ciclo Principal -+-+-+-+-+-+-+-+-+-+-+-

while Robot_1.step(timestep) != -1:
    left_motor.setVelocity(rev)
    right_motor.setVelocity(rev)

    # -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    # -+-+-+-+- Actualizar valores +-+-+-+
    ds_0_valor = ds_0.getValue()
    ds_2_valor = ds_2.getValue()
    ds_3_valor = ds_3.getValue()
    ds_4_valor = ds_4.getValue()
    ds_5_valor = ds_5.getValue()
    compass_valor = compass.getValues()
    PositionSensor_left_valor = PositionSensor_left.getValue()
    vueltas = PositionSensor_left_valor/(2*3.14)
    print("Vueltas: ",vueltas, "  Distancia: ", vueltas*2*3.14*r)

    #print(bearing(compass_valor))
    #Distancia(ds_0_valor)   