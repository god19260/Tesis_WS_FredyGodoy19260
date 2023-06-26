
from controller import Robot

class Slave(Robot):
    # get the time step of the current world.
    timestep = 5
    maxSpeed = 0.035 #mt/s
    r = 0.035 # radio en m 
    rev = maxSpeed/(2*3.14*r)*60
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
        PositionSensor_left = self.getDevice('PositionSensor_1')
        PositionSensor_left.enable(self.timestep)
        PositionSensor_right = self.getDevice('PositionSensor_2')
        PositionSensor_right.enable(self.timestep)

        # Habilitar sensores de distancia
        for dsnumber in range(0, 6):
            self.distanceSensors.append(self.getDevice('ds_' + str(dsnumber)))
            self.distanceSensors[-1].enable(self.timestep)
        
        # Habilitar compass
        self.compass = self.getDevice('compass')
        self.compass.enable(self.timestep)


    def run(self):
        while True:
            #ds0_valor = self.distanceSensors[0].getValue()
            self.DatosSensores()
            if self.ds0_valor > 20:
                self.left_motor.setVelocity(10)
                self.right_motor.setVelocity(10)
            else:
                self.left_motor.setVelocity(0)
                self.right_motor.setVelocity(0)
            # Perform a simulation step, quit the loop when
            # Webots is about to quit.
            if self.step(self.timestep) == -1:
                break
    def DatosSensores(self):
        # Actualizar sensores de distancia
        self.ds0_valor = self.distanceSensors[0].getValue()
        self.ds1_valor = self.distanceSensors[1].getValue()
        self.ds2_valor = self.distanceSensors[2].getValue()
        self.ds3_valor = self.distanceSensors[3].getValue()
        self.ds4_valor = self.distanceSensors[4].getValue()
        self.ds5_valor = self.distanceSensors[5].getValue()
controller = Slave()
controller.run()
