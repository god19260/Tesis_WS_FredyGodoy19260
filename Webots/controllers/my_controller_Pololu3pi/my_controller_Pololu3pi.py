
from controller import Robot
import numpy as np

class Slave(Robot):
    # get the time step of the current world.
    timestep = 5

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


    def run(self):
        while True:
            #ds0_valor = self.distanceSensors[0].getValue()
            self.DatosSensores()
            self.ControlOrientacion(2,2)
            
            """
            if self.ds0_value > 40:
                self.left_motor.setVelocity(10)
                self.right_motor.setVelocity(10)
            else:
                self.left_motor.setVelocity(0)
                self.right_motor.setVelocity(0)
            """
            
            # Perform a simulation step, quit the loop when
            # Webots is about to quit.
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
        print(self.rotz_g)

    def ControlOrientacion(self,xg,yg):
        # PID orientación
        kpO = 1*10
        kiO = 0.001 
        kdO = 0
        EO = 0
        eO_1 = 0
        eO = 1.0
        
        while eO > 0.01:
            self.DatosSensores()
            x = 0.5
            y = 0.5
            e = [xg-x, yg-y]
            #thetag = np.arctan2(e[1],e[0])
            thetag = 270/180*np.pi
            eO = thetag-self.rotz
            eO = abs(np.arctan2(np.sin(eO),np.cos(eO)))
            print("eO: ",eO)
            # Control de velocidad angular
            eO_D = eO - eO_1
            EO = EO + eO
            w = kpO*eO + kiO*EO + kdO*eO_D
            eO_1 = eO
            
            if eO >=0.01:
                giroder = (w*self.distanceCenter)/self.wheelRadius
                giroiz = -(w*self.distanceCenter)/self.wheelRadius

                if giroder >= 10:
                    giroder = 10
                if giroder <= -10:
                    giroder = -10

                if giroiz >= 10:
                    giroiz = 10
                if giroiz <= -10:
                    giroiz = -10

                self.right_motor.setVelocity(giroder)
                self.left_motor.setVelocity(giroiz)
            
            else:
                self.left_motor.setVelocity(0)
                self.right_motor.setVelocity(0)
            
            if self.step(self.timestep) == -1:
                break
        
controller = Slave()
controller.run()
