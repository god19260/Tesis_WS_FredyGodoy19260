
from controller import Robot

class Slave(Robot):
    # get the time step of the current world.
    timestep = 5
    maxSpeed = 0.035 #mt/s
    r = 0.035 # radio en m 
    rev = maxSpeed/(2*3.14*r)*60
    distanceSensor = []
    def __init__(self):
        left_motor = self.getDevice('motor_1')
        right_motor = self.getDevice('motor_2')
        
        left_motor.setPosition(float('inf'))
        left_motor.setVelocity(0.0)

        right_motor.setPosition(float('inf'))
        right_motor.setVelocity(0.0)

        PositionSensor_left = self.getDevice('PositionSensor_1')
        PositionSensor_left.enable(self.timestep)
        PositionSensor_right = self.getDevice('PositionSensor_2')
        PositionSensor_right.enable(self.timestep)

        
        for dsnumber in range(0, 8):
            self.distanceSensors.append(self.getDevice('ds_' + str(dsnumber)))
            self.distanceSensors[-1].enable(self.timeStep)
    def run():
        print("Todo bien")
controller = Slave()
controller.run()
