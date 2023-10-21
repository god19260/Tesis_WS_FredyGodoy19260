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
"""

Walls = []
translation_field = []
orientation_field = []
position = []

for dsnumber in range(0, 6):
    Walls.append(robot.getFromDef('wall(' + str(dsnumber)+')'))
    Walls[-1].getField('translation')
"""
wall = robot.getFromDef('wall(5)')
translation_field = wall.getField('translation')
rotation_field = wall.getField('rotation')

new_value = [0, 0, 0]
translation_field.setSFVec3f(new_value)

new_orientation = [0,0,1,3.14/2]
rotation_field.setSFRotation(new_orientation)

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
