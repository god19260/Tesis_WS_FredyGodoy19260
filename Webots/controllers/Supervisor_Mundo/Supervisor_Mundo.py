"""Supervisor_Mundo controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Supervisor
import numpy as np
# create the Robot instance.
robot = Supervisor()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname') 
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)


Walls = []
translation_field = []
orientation_field = []

Obs_Translation_Field = []
Obs_Orientation_Field = []
Obs = []


cant_paredes = 10
cant_cajas = 3

modo = 0 # 0 Obtener datos, 1 colocar paredes, 2 pruebas

# -'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'- Obtener objetos del mundo -'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-
# Paredes
for dsnumber in range(cant_paredes):
    Walls.append(robot.getFromDef('wall(' + str(dsnumber)+')'))
    translation_field.append(Walls[-1].getField('translation'))
    orientation_field.append(Walls[-1].getField('rotation'))

# Obstaculos: Cajas
for box_number in range(cant_cajas):
    Obs.append(robot.getFromDef('BOX_'+str(box_number)))
    Obs_Translation_Field.append(Obs[box_number].getField('translation'))
    Obs_Orientation_Field.append(Obs[box_number].getField('rotation'))


# -'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-


# -'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'- Modos -'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-
if modo == 0:
    # Obtener datos de las paredes:
    # Obtener las posiciones de las paredes 
    print(" \nPosiciones de las paredes")
    for i in range(len(Walls)):
        print('wall(',i,'): ',Walls[i].getPosition())
        
    # Obtener la orientación de las paredes 
    print(' \nOrientación de las paredes')
    for i in range(len(Walls)):
        print('wall(',i,'): ',orientation_field[i].getSFVec3f())

    # Obtener datos de las cajas
    # Obtener las posiciones de las cajas
    print(" \nPosiciones de las cajas")
    for i in range(len(Obs)):
        print('Obstaculo Caja ',i,': ', Obs[i].getPosition())

    # Obtener la orientación de las cajas
    print(' \nOrientación de las cajas')
    for i in range(len(Obs)):
        print('Obstaculo Caja ',i,': ', Obs_Orientation_Field[i].getSFVec3f())

elif modo == 1:
    # Mapa: Validación de algoritmos independientes
    Walls_Positions =[[0.58, -1.09, 0.0],
            [-2.13, -0.49999, 0.0],
            [-1.09, 1.46, 0.0],
            [-0.03, -2.32, 0.0],
            [-0.130006, 0.49001, 0.0],
            [0.33, -0.48, 0.0],
            [0.300002, 1.50001, 0.0],
            [0.76, 0.46, 0.0],
            [-0.91, 2.46, 0.0],
            [0.65999, 1.5, 0.0]]

    Walls_Orientations = [[0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 1.0, 1.5708],
                        [0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 1.0, 1.5708],
                        [0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 1.0, 1.5708],
                        [0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 1.0, 1.5708]]


    for i in range(len(Walls)):
        new_translation = Walls_Positions[i]
        translation_field[i].setSFVec3f(new_translation)

        new_orientation = Walls_Orientations[i]
        orientation_field[i].setSFRotation(new_orientation)

# -'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-'-


# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
