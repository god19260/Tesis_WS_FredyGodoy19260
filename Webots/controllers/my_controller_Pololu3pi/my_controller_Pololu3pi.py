
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
        fGeneral = False
        self.angulo = 270
        self.dMin = 15 # Distancia minima del objeto en cm

        while self.step(self.timestep) != -1:
            if fGeneral:
                self.DatosSensores()
                
                # Desición de Giro
                self.DesicionGiro()
                self.RotControl(self.angulo)
                

                # Avanzar hacia adelante hasta determinar un cambio de trayectoria               
                while (self.ds0_value > self.ds1_value or self.ds0_value > self.ds2_value) and (self.ds0_value > self.ds4_value or self.ds0_value > self.ds5_value):
                    self.DatosSensores()

                    # Otras condiciones para cambiar de giro 
                    if self.ds5_value < 18 or self.ds1_value < 18:
                        break
                    # Freno de emergencia
                    if self.ds0_value < self.dMin:
                        break

                    self.left_motor.setVelocity(10)
                    self.right_motor.setVelocity(10)
                
                    # Perform a simulation step, quit the loop when
                    # Webots is about to quit.
                    if self.step(self.timestep) == -1:
                        break

                self.left_motor.setVelocity(0)
                self.right_motor.setVelocity(0)
                """
                # Desición de giro
                if self.ds0_value < dMin and self.ds4_value < self.ds2_value and self.ds5_value < self.ds1_value:
                    angulo = angulo-90
                    print("1")
                elif self.ds0_value < dMin and self.ds1_value < self.ds5_value and self.ds2_value < self.ds4_value:
                    angulo = angulo+90
                    print("2")
                elif self.ds0_value < dMin and self.ds1_value > dMin and self.ds2_value > dMin and self.ds4_value > dMin and self.ds5_value > dMin:
                    angulo = angulo+90
                    print("3")
                """

            fGeneral = True  # Bandera general del proceso
            
           
        
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

    def RotControl(self,rotz):
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
            #e = [xg-x, yg-y]
            #thetag = np.arctan2(e[1],e[0])
            thetag = rotz/180*np.pi
            eO = thetag-self.rotz
            eO = np.arctan2(np.sin(eO),np.cos(eO))
            if eO >0:
                flag_dGiro = True  # bandera dirección del giro, 
                                   # True = sentido horario
                                   # False = sentido antihorario
            else:
                flag_dGiro = False
            eO = abs(eO)
            # Control de velocidad angular
            eO_D = eO - eO_1
            EO = EO + eO
            w = kpO*eO + kiO*EO + kdO*eO_D
            eO_1 = eO
            
            if eO >=0.01:
                if flag_dGiro == True:
                    giroder = (w*self.distanceCenter)/self.wheelRadius
                    giroiz = -(w*self.distanceCenter)/self.wheelRadius
                else: 
                    giroder = -(w*self.distanceCenter)/self.wheelRadius
                    giroiz = (w*self.distanceCenter)/self.wheelRadius

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
    def DesicionGiro(self):
        # Función para determinar la siguiente acción de giro
        if self.ds1_value > self.ds0_value and self.ds1_value > self.ds5_value and self.ds2_value > self.dMin +10:
            self.angulo = self.angulo - 45
            print("giro 1")
        elif self.ds5_value > self.ds0_value and self.ds5_value > self.ds1_value and self.ds4_value > self.dMin +10:
            self.angulo = self.angulo + 45
            print("giro 2")
        elif self.ds3_value > self.ds0_value and self.ds3_value > self.ds1_value and self.ds3_value > self.ds2_value and self.ds3_value > self.ds4_value and self.ds3_value > self.ds5_value:
            self.angulo = self.angulo + 180
            print("giro 3")
        elif self.ds1_value <= self.dMin+3:
            print("giro 4")
            self.angulo = self.angulo + 45
            self.RotControl(self.angulo)
            self.DatosSensores()
            if self.ds5_value < 30:
                while self.ds0_value > self.dMin:
                    self.DatosSensores()
                    self.left_motor.setVelocity(10)
                    self.right_motor.setVelocity(10)
                    print("while de giro 4")
                    # Perform a simulation step, quit the loop when
                    # Webots is about to quit.
                    if self.step(self.timestep) == -1:
                        break

        elif self.ds5_value <= self.dMin+3:
            print("giro 5")
            self.angulo = self.angulo - 45
            self.RotControl(self.angulo)
            self.DatosSensores()
            if self.ds5_value < 30:
                while self.ds0_value > self.dMin:
                    self.DatosSensores()
                    self.left_motor.setVelocity(10)
                    self.right_motor.setVelocity(10)
                    print("while de giro 5")
                    # Perform a simulation step, quit the loop when
                    # Webots is about to quit.
                    if self.step(self.timestep) == -1:
                        break



            
controller = Slave()
controller.run()
