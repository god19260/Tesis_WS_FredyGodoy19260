
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
    
    # Variables para determinar la distancia en linea recta de un trayecto en especifico
    distAnterior_Right = 0
    distAnterior_Left = 0

    # Trayectoria de la exploración separada en coordenadas
    T_Exploracion_x = []
    T_Exploracion_y = []

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
        self.rangoSenDis = 50 # Distancia máxima de sensado
        self.avanzar = False
        while self.step(self.timestep) != -1:
            if fGeneral:
                self.DatosSensores()            
                self.DecisionGiro()
                self.RotControl(self.angulo)                  
                
                self.DistanciaLineaRecta_Inicio()
                self.Explorar()
                self.DistanciaLineaRecta_Fin()
                self.TrayectoriaExploracion(self)
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

        # Actualizar valores de sensores de posición de las ruedas
        self.PS_Right_value = self.PositionSensor_right.getValue()  # PS_Right_value --> position sensor right value
        self.PS_Left_value = self.PositionSensor_left.getValue()  # PS_Left_value --> position sensor leftt value 
        self.revsRight = self.PS_Right_value/(2*np.pi)
        self.revsLeft = self.PS_Left_value/(2*np.pi)
        self.DRW_Right = self.revsRight*2*np.pi*self.wheelRadius# Distancia recorrida por la llanta derecha
        self.DRW_Left = self.revsLeft*2*np.pi*self.wheelRadius# Distancia recorrida por la llanta izquierda


    def RotControl(self,rotz):
        print("Función: Rot Control")
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
    
    def DecisionGiro(self):
        #print("Función: Decisión giro")
        # Función para determinar la siguiente acción de giro
        if self.ds1_value >= self.ds5_value and self.ds1_value >= self.dMin+3 and self.ds2_value >= self.dMin+3:
            self.angulo = self.angulo -45
            #print("giro 1")
        elif self.ds5_value >= self.ds1_value and self.ds5_value >= self.dMin+3 and self.ds4_value>= self.dMin+3:
            self.angulo = self.angulo + 45
            #print("giro 2")   
            
        elif self.ds1_value > self.ds0_value and self.ds1_value > self.ds2_value and self.ds1_value > self.ds3_value and self.ds1_value > self.ds4_value and self.ds1_value > self.ds5_value:
            self.angulo = self.angulo-45
            #print("giro 3")
        elif self.ds5_value > self.ds0_value and self.ds5_value > self.ds1_value and self.ds5_value > self.ds2_value and self.ds5_value > self.ds3_value and self.ds5_value > self.ds4_value:
            self.angulo = self.angulo+45
            #print("giro 4")

        elif self.ds3_value > self.ds0_value and self.ds3_value > self.ds1_value and self.ds3_value > self.ds2_value and self.ds3_value > self.ds4_value and self.ds3_value > self.ds5_value:
            self.angulo = self.angulo +180
            #print("giro 5") 
        
        elif self.ds1_value <= self.dMin+3 and self.ds5_value >= self.dMin+20:
            self.angulo = self.angulo +45
            #print("giro 6") 
        elif self.ds5_value <= self.dMin+3 and self.ds1_value >= self.dMin+20:
            self.angulo = self.angulo -45
            #print("giro 7") 
        
        else:
            # avanzar hasta proxima condición de giro
            self.avanzar = True
            #print("++++ No se cambio el giro")
    
    def Explorar(self):
        while (self.ds0_value >= self.ds1_value or self.ds2_value < self.dMin+3) and (self.ds0_value >= self.ds5_value or self.ds4_value < self.dMin+3) or self.avanzar:
            # Actualizar los valores de los sensores
            self.DatosSensores()  

            self.left_motor.setVelocity(10)
            self.right_motor.setVelocity(10)
            
            # Condiciones especiales para cambiar la rotación
            if self.ds0_value <= self.dMin+3 or self.ds1_value <= self.dMin or self.ds5_value <= self.dMin:
                print("---- Freno de emergencia ----")
                self.avanzar = False
                break                   
            
            if self.step(self.timestep) == -1:
                break

        self.left_motor.setVelocity(0)
        self.right_motor.setVelocity(0)

    def DistanciaLineaRecta_Inicio(self):
        # Guardar distancia actual para iniciar el proceso de medición
        self.distAnterior_Right = self.DRW_Right
        self.distAnterior_Left = self.DRW_Left
    def DistanciaLineaRecta_Fin(self):
        # llanta derecha
        self.distActual_Right = self.DRW_Right
        self.d_lineaRecta_Right = self.distActual_Right-self.distAnterior_Right
        

        # llanta izquierda
        self.distActual_Left = self.DRW_Left
        self.d_lineaRecta_Left = self.distActual_Left-self.distAnterior_Left
        
        self.promedio_distancia_trayecto = (self.d_lineaRecta_Left+self.d_lineaRecta_Right)/2
        print(self.d_lineaRecta_Left,"  ",self.d_lineaRecta_Right, "  ",self.promedio_distancia_trayecto)
    
    def TrayectoriaExploracion(self):
        self.T_Exploracion_x.append(np.cos(self.angulo)*self.promedio_distancia_trayecto) # Trayectoria exploración coordenada en x
        self.T_Exploracion_y.append(np.sin(self.angulo)*self.promedio_distancia_trayecto) # Trayectoria exploración coordenada en y

controller = Slave()
controller.run()
