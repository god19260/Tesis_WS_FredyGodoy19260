"""my_controller_EpuckPruebas controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor


from controller import Robot
from Funciones import velocidad

Robot_1 = Robot()


# get the time step of the current world.
timestep = 5
maxSpeed = 10
   
# Configuraciones
left_motor = Robot_1.getDevice('motor_1')
right_motor = Robot_1.getDevice('motor_2')

left_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)

right_motor.setPosition(float('inf'))
right_motor.setVelocity(0.0)

while Robot_1.step(timestep) != -1:
    left_motor.setVelocity(maxSpeed)
    right_motor.setVelocity(maxSpeed)
    velocidad(maxSpeed)