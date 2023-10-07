
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

    # Especificaciones del mundo
    size_x = 5 #mt
    size_y = 5 #mt

    # Caracteristicas del robot
    maxSpeed = 0.035 #mt/s
    wheelRadius = 0.035 #radio en m 
    distanceCenter = 0.075 #m
    rev = maxSpeed/(2*3.14*wheelRadius)*60
    
    # Variables para determinar la distancia en linea recta de un trayecto en especifico
    distAnterior_Right = 0
    distAnterior_Left = 0

    # Trayectoria de la exploración separada en coordenadas
    x_vehiculo = 0
    y_vehiculo = 0
    T_Exploracion_x = [0]
    T_Exploracion_y = [0]

    Distancias_lineaRecta = []
    Angulos = []
    Distancia_Total = 0
    
    # Banderas para activación desde teclado
    showMap = False
    showStats = False
    show_WS = False
    WS_2D_3D = False
    WS_Trayec_2D_3D = False
    Tray_Control = False

    # Definiciones previas
    distanceSensors = []
    nodos_GPS_x = []
    nodos_GPS_y = []
    error_GPS_revs = []
    delta_GPS_revs_x = 0
    delta_GPS_revs_y = 0

    # mapeo de paredes
    rango_max_dsen = 199 #cm
    Pared_x_ds0 = []
    Pared_x_ds1 = []
    Pared_x_ds2 = []
    Pared_x_ds3 = []
    Pared_x_ds4 = []
    Pared_x_ds5 = []

    Pared_y_ds0 = []
    Pared_y_ds1 = []
    Pared_y_ds2 = []
    Pared_y_ds3 = []
    Pared_y_ds4 = []
    Pared_y_ds5 = []
    
    #Espacio de trabajo 
    WS_x = []
    WS_y = []
    min_val_x = 0
    min_val_y = 0
    #mapa_WS = np.array([])
    
    #*-*-*-*-*-*-*-*-* Valores iniciales *-*-*-*-*-*-*-*-*-*
    f_ValoresIniciales = True # Bandera valores iniciales 
    # sensores de posición de los motores
    PS_Right_StartValue = 0
    PS_Left_StartValue = 0

    # Función de odometría
    PS_Right_Anterior = 0
    PS_Left_Anterior = 0
    
    phi = 0
    xc = [0]
    yc = [0]
    #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

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
        print("m: mostrar mapa\ns: mostrar stats\nw: mostrar espacio de trabajo")
        print("\n1: mostrar WS en 2D y 3D\n2: mostrar trayectoria óptima")
        fGeneral = False
        self.angulo = 90
        self.phi = self.angulo # funcion de odometria
        self.dMin = 13 # Distancia minima del objeto en cm
        self.rangoSenDis = 50 # Distancia máxima de sensado
        self.avanzar = False
        fValoresIniciales = True

        while self.step(self.timestep) != -1:
            if fGeneral:
                self.DatosSensores()            
                self.DecisionGiro()
                self.RotControl(self.angulo)  

                self.Explorar()
                #self.Initial_Run_Ex()
                self.Graficas()
                
            else:
                self.DatosSensores()            
                self.Initial_Run_Ex()
                fGeneral = True  # Bandera general del proceso
                 
    def DatosSensores(self):
        if  self.f_ValoresIniciales:
            # Sensores de posición de los motores
            self.PS_Right_StartValue =  self.PositionSensor_right.getValue()  # PS_Right_value --> position sensor right value
            self.PS_Left_StartValue =  self.PositionSensor_left.getValue()  # PS_Right_value --> position sensor right value
            
            # GPS: valores iniciales para trayectoria de exploración con datos de GPS
            self.GPS_values = self.GPS.getValues()
            self.nodos_GPS_x.append(self.GPS_values[0]+self.size_x/2)
            self.nodos_GPS_y.append(self.GPS_values[1]+self.size_y/2)
           

            self.f_ValoresIniciales = False

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

    def RotControl(self,rotz):
        #print("Función: Rot Control")
        # PID orientación
        kpO = 15 #15
        kiO = 0.001 
        kdO = 1 #1
        EO = 0
        eO_1 = 0
        eO = 1.0
        
        while eO > 0.003:
            self.DatosSensores()
            self.Odometria()
            self.Paredes(self.rotz*180/np.pi)
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
            
            if eO >=0.003:
                if flag_dGiro == True:
                    giroder = (w*self.distanceCenter)/self.wheelRadius
                    giroiz = -(w*self.distanceCenter)/self.wheelRadius
                else: 
                    giroder = -(w*self.distanceCenter)/self.wheelRadius
                    giroiz = (w*self.distanceCenter)/self.wheelRadius

                if giroder >= 0.5:
                    giroder = 0.5
                    giroiz = -0.5
                elif giroder <= -0.5:
                    giroder = -0.5
                    giroiz = 0.5
                
                """
                if giroiz >= 0.5:
                    giroiz = 0.5
                elif giroiz <= -0.5:
                    giroiz = -0.5
                """

                self.right_motor.setVelocity(giroder)
                self.left_motor.setVelocity(giroiz)
            
            else:
                self.left_motor.setVelocity(0)
                self.right_motor.setVelocity(0)
            
            if self.step(self.timestep) == -1:
                break
            
    def DecisionGiro(self):
        #print(self.angulo, "   -   ", self.rotz_g)
        # Función para determinar la siguiente acción de giro
        
        if self.avanzar == False:
            if self.ds1_value <= self.dMin:
                self.angulo +=45

            if self.ds5_value <= self.dMin:
                self.angulo -=45
            return
        
        
        dis = 100
        #if self.ds0_value < dis:                  
        if self.ds1_value > self.ds0_value:
            self.angulo = self.angulo -45
            #print("giro 1")
            
        elif self.ds5_value > self.ds0_value:
            self.angulo = self.angulo +45
            #print("giro 2")

        elif self.ds0_value < 70 and self.ds3_value > self.ds0_value and self.ds3_value > self.ds1_value and self.ds3_value > self.ds5_value:
            self.angulo += 180 
            #print("giro 3, 180°") 
              
        else:
            
            numero_aleatorio = random.randint(0, 1)
            if numero_aleatorio == 1:
                self.angulo -= 45
            else:
                self.angulo += 90
            
            #self.angulo += 90
            #print("giro 3, 180°")  
        
        """
        self.angulo= self.angulo % 360
        if self.angulo > 180:
            self.angulo -= 360
        elif self.angulo < -180:
            self.angulo += 360
        """
        """
        if self.ds1_value >= self.ds0_value and self.ds1_value >= self.ds5_value:
            if self.ds2_value >= self.ds4_value and self.ds2_value >= self.ds0_value and self.ds1_value >= self.dMin and self.ds2_value >= self.dMin:
                self.angulo = self.angulo -45
                print("giro 1")
                return

        elif self.ds5_value >= self.ds0_value and self.ds5_value >= self.ds1_value:
            if self.ds4_value >= self.ds2_value and self.ds4_value >= self.ds0_value and self.ds5_value >= self.dMin and self.ds4_value>= self.dMin:
                self.angulo = self.angulo + 45
                print("giro 2")   
                return
            
        if self.ds1_value >= self.ds0_value and self.ds2_value >= self.dMin+1:
            self.angulo = self.angulo-45
            print("giro 3")
            return
        
        if self.ds5_value > self.ds0_value and self.ds4_value > self.dMin+1:
            self.angulo = self.angulo+45
            print("giro 4")
            return
        
        
        if self.ds3_value > self.ds0_value and self.ds3_value > self.ds1_value and self.ds3_value > self.ds2_value and self.ds3_value > self.ds4_value and self.ds3_value > self.ds5_value:
            self.angulo = self.angulo +180
            print("giro 5") 
            return
            

        # avanzar hasta proxima condición de giro
        self.avanzar = True
        self.angulo = self.angulo -180
        print("++++ GIRO FORZADO ")
        """

    def Explorar(self):
     
        self.avanzar = True
        self.cont = 0
        self.coef_velocidad = 0.01
        self.vel_max = 4
        self.ds0_min_val = 30
        while (self.ds0_value >= self.ds2_value) and (self.ds0_value >= self.ds4_value) or self.ds0_value>self.ds0_min_val:
            
            # Verificar si se presiona una tecla 
            self.KeyPress_Flag()

            self.DistanciaLineaRecta_Inicio()
            self.left_motor.setVelocity(self.vel_max*self.coef_velocidad)
            self.right_motor.setVelocity(self.vel_max*self.coef_velocidad)
            if self.coef_velocidad < 1:
                self.coef_velocidad += 0.05
            # Actualizar los valores de los sensores
            self.DatosSensores()
            self.Odometria()
            
            self.DistanciaLineaRecta_Fin()
            self.TrayectoriaExploracion()
            self.Paredes(self.angulo)
           
            if self.ds2_value < 100 and self.ds4_value < 100:
                self.ds0_min_val = 30
            else:
                self.ds0_min_val = 100

            if self.cont == 9:
                self.RotControl(self.angulo)
                self.cont = 0
            self.cont +=1        
            
            # Condiciones especiales para cambiar la rotación
            if self.ds0_value <= self.dMin or self.ds1_value <= self.dMin or self.ds5_value <= self.dMin:
                print("---- Freno de emergencia ----")
                self.avanzar = False
                
                while self.coef_velocidad > 0.1:
                    self.left_motor.setVelocity(self.vel_max*self.coef_velocidad)
                    self.right_motor.setVelocity(self.vel_max*self.coef_velocidad)
                    self.coef_velocidad -= 0.5
                self.left_motor.setVelocity(0)
                self.right_motor.setVelocity(0)
                break                   
            
            if self.step(self.timestep) == -1:
                break
        while self.coef_velocidad > 0:
            self.left_motor.setVelocity(self.vel_max*self.coef_velocidad)
            self.right_motor.setVelocity(self.vel_max*self.coef_velocidad)
            self.coef_velocidad -= 0.05

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
        self.Distancias_lineaRecta.append(self.promedio_distancia_trayecto)
        self.Angulos.append(self.angulo)
        #print(self.d_lineaRecta_Left,"  ",self.d_lineaRecta_Right, "  ",self.promedio_distancia_trayecto)
    
    def TrayectoriaExploracion(self):
        self.Distancia_Total += self.promedio_distancia_trayecto
       
        self.x_vehiculo = self.T_Exploracion_x[len(self.T_Exploracion_x)-1]+np.cos(self.angulo*np.pi/180)*self.promedio_distancia_trayecto
        self.y_vehiculo = self.T_Exploracion_y[len(self.T_Exploracion_y)-1]+np.sin(self.angulo*np.pi/180)*self.promedio_distancia_trayecto

        self.T_Exploracion_x.append(self.x_vehiculo) # Trayectoria exploración coordenada en x
        self.T_Exploracion_y.append(self.y_vehiculo) # Trayectoria exploración coordenada en y 

        #print(np.sin(self.angulo*np.pi/180), "  ", self.angulo )
        
        # valores obtenidos con base al sensor GPS de webots 
        self.nodos_GPS_x.append(self.GPS_values[0]+self.size_x/2)
        self.nodos_GPS_y.append(self.GPS_values[1]+self.size_y/2)

        # porcentaje de error
        self.delta_GPS_revs_x = abs(0-self.nodos_GPS_x[0])
        self.delta_GPS_revs_y = abs(0-self.nodos_GPS_y[0])
        
        v_aproximado = np.sqrt((self.T_Exploracion_x[len(self.T_Exploracion_x)-1]+self.delta_GPS_revs_x)**2+(self.T_Exploracion_y[len(self.T_Exploracion_y)-1]+self.delta_GPS_revs_y)**2)
        v_real = np.sqrt(self.nodos_GPS_x[len(self.nodos_GPS_x)-1]**2 +self.nodos_GPS_y[len(self.nodos_GPS_y)-1]**2)
        #v_aproximado = round(self.y_vehiculo+self.delta_GPS_revs_y,4)
        #v_real = round(self.GPS_values[1]+self.size_y/2,4) 

        self.error_GPS_revs.append(abs((v_aproximado-v_real)/abs(v_real))*100)
        #print(self.GPS_values[0]+self.size_x/2," -- ",self.GPS_values[1]+self.size_y/2," || ",self.x_vehiculo+self.delta_GPS_revs_x," -- ",self.y_vehiculo+self.delta_GPS_revs_y)

    def Paredes(self,angulo):
        #print(len(self.T_Exploracion_x) , " -- ",len(self.T_Exploracion_y) , " -- " ,len(self.Pared_x) , " -- ",len(self.Pared_y))
        if self.ds0_value<self.rango_max_dsen:
            x = self.ds0_value*np.cos((angulo)*np.pi/180)/100
            y = self.ds0_value*np.sin((angulo)*np.pi/180)/100
            
            self.Pared_x_ds0.append(self.T_Exploracion_x[len(self.T_Exploracion_x)-1]+x)
            self.Pared_y_ds0.append(self.T_Exploracion_y[len(self.T_Exploracion_y)-1]+y)

        if self.ds2_value<self.rango_max_dsen:
            x = self.ds2_value*np.cos((angulo-90)*np.pi/180)/100
            y = self.ds2_value*np.sin((angulo-90)*np.pi/180)/100
            
            self.Pared_x_ds2.append(self.T_Exploracion_x[len(self.T_Exploracion_x)-1]+x)
            self.Pared_y_ds2.append(self.T_Exploracion_y[len(self.T_Exploracion_y)-1]+y)
        
        if self.ds4_value<self.rango_max_dsen:
            x = self.ds4_value*np.cos((angulo+90)*np.pi/180)/100
            y = self.ds4_value*np.sin((angulo+90)*np.pi/180)/100
            
            self.Pared_x_ds4.append(self.T_Exploracion_x[len(self.T_Exploracion_x)-1]+x)
            self.Pared_y_ds4.append(self.T_Exploracion_y[len(self.T_Exploracion_y)-1]+y)
        
        if self.ds1_value<self.rango_max_dsen:
            x = self.ds1_value*np.cos((angulo-45)*np.pi/180)/100
            y = self.ds1_value*np.sin((angulo-45)*np.pi/180)/100
            
            self.Pared_x_ds1.append(self.T_Exploracion_x[len(self.T_Exploracion_x)-1]+x)
            self.Pared_y_ds1.append(self.T_Exploracion_y[len(self.T_Exploracion_y)-1]+y)
        
        if self.ds5_value<self.rango_max_dsen:
            x = self.ds5_value*np.cos((angulo+45)*np.pi/180)/100
            y = self.ds5_value*np.sin((angulo+45)*np.pi/180)/100
            
            self.Pared_x_ds5.append(self.T_Exploracion_x[len(self.T_Exploracion_x)-1]+x)
            self.Pared_y_ds5.append(self.T_Exploracion_y[len(self.T_Exploracion_y)-1]+y)

    def Graficas(self):
        # Verificar si se presiona una tecla
        self.KeyPress_Flag()

        if self.showMap == True:
            self.showMap = False
            #print(self.T_Exploracion_x[len(self.T_Exploracion_x)-1]+self.delta_GPS_revs_x ,'  ' , self.nodos_GPS_x[len(self.nodos_GPS_x)-1])
            
            # Crear una figura 
            self.fig = plt.figure()
            self.fig.suptitle('Trayectoria Exploración')
            
            # *-*-*-*-*-*-*-*-*-*-*-*-* Crear una subfigura *-*-*-*-*-*-*-*-*-*-*-*-*   
            # (Trayectoria experimental, obtenida de las revoluciones de las ruedas)
            self.ax1 = self.fig.add_subplot(121)

            # Configurar límites de los ejes
            self.ax1.set_xlim(0, self.size_x*10)
            self.ax1.set_ylim(0, self.size_y*10)

            # Configurar aspecto de los ejes
            self.ax1.set_aspect('equal')
            self.ax1.grid(True)
            
            
            plt.plot(self.T_Exploracion_x, self.T_Exploracion_y, '-o', color='red')
            #plt.plot(self.Pared_x_ds2,self.Pared_y_ds2,'o', color='black')
            #plt.plot(self.Pared_x_ds4,self.Pared_y_ds4,'o', color='black')
            #plt.plot(self.Pared_x_ds0,self.Pared_y_ds0,'o', color='black')

            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title('Por posición de ruedas')
            plt.xlim(0,5)
            plt.ylim(0,5)
            plt.grid(True)

            
            # *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*- 
            # *-*-*-*-*-*-*-*-*-*-*-*-* Crear otra subfigura *-*-*-*-*-*-*-*-*-*-*-*-*   
            #            (Trayectoria Teórica, obtenida por el GPS del robot)
            self.ax2 = self.fig.add_subplot(122)

            # Configurar límites de los ejes
            self.ax2.set_xlim(0, self.size_x*10)
            self.ax2.set_ylim(0, self.size_y*10)

            # Configurar aspecto de los ejes
            self.ax2.set_aspect('equal')
            self.ax2.grid(True)
            
            plt.plot(self.nodos_GPS_x, self.nodos_GPS_y, '-o', color='green')
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title('GPS')
            plt.xlim(0,5)
            plt.ylim(0,5)
            plt.grid(True)
            # *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*- 
            # *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*- 
        
        if self.showStats == True: 
            print("Distancia total recorrida: ", self.Distancia_Total)
            self.showStats = False  
            # ------------------------- Crear una figura -------------------------- 
            # */*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
            # */*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
            self.fig2 = plt.figure()
            self.fig2.suptitle('Errores y coordenadas')
            # */*/*/*/*/*/*/*/*/*/*/*/* Crear una subfigura */*/*/*/*/*/*/*/*/*/*/*
            self.ax1_fig2 = self.fig2.add_subplot(121)

            # Configurar límites de los ejes
            self.ax1_fig2.set_xlim(0,len(self.nodos_GPS_x))
            self.ax1_fig2.set_ylim(0,100)

            # Configurar aspecto de los ejes
            
            self.ax1_fig2.grid(True)
            
            plt.title('Error acumulado')
            plt.plot(self.error_GPS_revs, color='blue')
            plt.xlabel('no. de nodos')
            plt.ylabel('Porcentaje de error')  
               
        
            # */*/*/*/*/*/*/*/*/*/*/*/* Crear otra subfigura */*/*/*/*/*/*/*/*/*/*/*
            self.ax2_fig2 = self.fig2.add_subplot(122)

            # Configurar límites de los ejes
            self.ax2_fig2.set_xlim(0,len(self.T_Exploracion_x))
            self.ax2_fig2.set_ylim(0,4)

            # Configurar aspecto de los ejes
            self.ax2_fig2.grid(True)
            
            plt.title('Coordenadas x: GPS vs por posición de ruedas')
            plt.plot(self.T_Exploracion_x, color='red')
            plt.plot(self.nodos_GPS_x, color='blue')
            plt.xlabel('Coordenadas x: GPS (rojo) y por posición de ruedas (azul)')
            plt.ylabel('mt')  
            
            
            # */*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
            """
            # */*/*/*/*/*/*/*/*/*/*/*/* Crear otra subfigura */*/*/*/*/*/*/*/*/*/*/*
            self.ax3_fig2 = self.fig2.add_subplot(133)

            # Configurar límites de los ejes
            self.ax3_fig2.set_xlim(0,len(self.T_Exploracion_y))
            self.ax3_fig2.set_ylim(0,5)

            # Configurar aspecto de los ejes
            self.ax3_fig2.grid(True)
            
            plt.title('Coordenadas y: GPS vs por posición de ruedas')
            plt.plot(self.T_Exploracion_y, color='red')
            plt.plot(self.nodos_GPS_y, color='blue')
            plt.xlabel('Coordenadas y: GPS (rojo) y por posición de ruedas (azul)')
            plt.ylabel('mt')  
            # */*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
            # */*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
            """
        
        if self.show_WS == True:
            self.show_WS = False
            self.EspacioTrabajo()
            # ------------------------- Crear una figura -------------------------- 
            # */*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
            # */*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
            self.fig3 = plt.figure()
            self.fig3.suptitle('Espacio de trabajo')
            # */*/*/*/*/*/*/*/*/*/*/*/* Crear una subfigura */*/*/*/*/*/*/*/*/*/*/*
            self.ax1_fig3 = self.fig3.add_subplot(121)

            # Configurar límites de los ejes
            self.ax1_fig3.set_xlim(-5,50)
            self.ax1_fig3.set_ylim(-5,50)

            # Configurar aspecto de los ejes
            self.ax1_fig3.set_aspect('equal')
            self.ax1_fig3.grid(True)
            
            plt.title('mapa 2D')
            plt.plot(self.WS_x,self.WS_y,'.',color='blue')
            plt.plot((self.factorWS*self.x_vehiculo),(self.factorWS*self.y_vehiculo),'o',color = 'red')
            plt.xlabel('x')
            plt.ylabel('y')     
            # */*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
            # *-*-*-*-*-*-*-*-*-*-*-*-* Crear una subfigura *-*-*-*-*-*-*-*-*-*-*-*-*   
            # (Trayectoria experimental, obtenida de las revoluciones de las ruedas)
            self.ax2_fig3 = self.fig3.add_subplot(122)

            # Configurar límites de los ejes
            self.ax2_fig3.set_xlim(0, self.size_x*10)
            self.ax2_fig3.set_ylim(0, self.size_y*10)

            # Configurar aspecto de los ejes
            self.ax2_fig3.set_aspect('equal')
            self.ax2_fig3.grid(True)
            
            
            
            plt.plot(self.Pared_x_ds2,self.Pared_y_ds2,'o', color='black')
            plt.plot(self.Pared_x_ds4,self.Pared_y_ds4,'o', color='black')
            plt.plot(self.Pared_x_ds0,self.Pared_y_ds0,'o', color='black')
            plt.plot(self.Pared_x_ds1,self.Pared_y_ds1,'o', color='black')
            plt.plot(self.Pared_x_ds5,self.Pared_y_ds5,'o', color='black')
            plt.plot((self.x_vehiculo),(self.y_vehiculo),'o',color = 'red')
            
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title('Por posición de ruedas')
            plt.xlim(0,5)
            plt.ylim(0,5)
            plt.grid(True)

            
            # *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*- 
            # */*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/* 
        
        if self.WS_2D_3D == True:
            self.WS_2D_3D = False
            self.Mapa_WS_2D_3D()
            
        if self.WS_Trayec_2D_3D == True:
            self.WS_Trayec_2D_3D = False
            
            self.Mapa_WS_Trayec_2D_3D()
            while not(keyboard.is_pressed("n")) and not(keyboard.is_pressed("3")):
                None
            self.KeyPress_Flag()

        if self.Tray_Control == True:
            self.Tray_Control = False
            # -+-+- Actualizción de variables para realizar el seguimiento de trayectoria
            self.phi = int(self.angulo)
            
            self.xc.clear()
            self.xc.append(self.x_vehiculo)

            self.yc.clear()
            self.yc.append(self.y_vehiculo)
            """
            while True:
                if self.step(self.timestep) == -1:
                    break
            """
            xGoal = self.x_rutaOptima
            yGoal = self.y_rutaOptima
            print(xGoal[len(xGoal)-1]-int(-self.min_val_x),'  ', yGoal[len(yGoal)-1]-int(-self.min_val_y))
            
            
            # Seguir la trayectoria
            self.Control_pos()   
            print("Pos actual odo: ",self.xc[len(self.xc)-1],"  ",self.yc[len(self.yc)-1])
            
            
            self.RotControl(self.angulo) 

        plt.show()
        
    def Initial_Run_Ex(self):
        for i in [45,45,45,45,45,45,45,45]:
            self.angulo += i
            self.RotControl(self.angulo)

    def EspacioTrabajo(self):
        #print(" *-*-*-*-*-* Determinar espacio de trabajo *-*-*-*-*-*")
        cant_columnas = 0
        cant_filas = 0
        self.factorWS = 9 # cada recuadro del mapa es de dimensiones (factor x factor)
        """
        d_sensors = [[self.Pared_x_ds0,self.Pared_y_ds0],
                     [self.Pared_x_ds1,self.Pared_y_ds1],
                     [self.Pared_x_ds2,self.Pared_y_ds2],
                     [self.Pared_x_ds3,self.Pared_y_ds3],
                     [self.Pared_x_ds4,self.Pared_y_ds4],
                     [self.Pared_x_ds5,self.Pared_y_ds5],
                     ]
        """
        d_sensors = [[self.Pared_x_ds0,self.Pared_y_ds0],
                     [self.Pared_x_ds1,self.Pared_y_ds1],
                     [self.Pared_x_ds2,self.Pared_y_ds2],
                     [self.Pared_x_ds4,self.Pared_y_ds4],
                     [self.Pared_x_ds5,self.Pared_y_ds5]
                     ]
        #WS_x = []
        #WS_y = []
        #mapa_WS = []

        # preparar arrays para el espacio de trabajo
        self.WS_x.clear()
        self.WS_y.clear()

        for d_sensor in d_sensors:
            x_ds = d_sensor[0] # x de distance sensor 
            y_ds = d_sensor[1] # y de distance sensor 
    
            ws_origen_x, ws_origen_y = [],[]

            for x in x_ds:
                self.WS_x.append(int(x*self.factorWS))
                if int(x*self.factorWS) < self.min_val_x:
                    self.min_val_x = int(x*self.factorWS)

            for y in y_ds:
                self.WS_y.append(int(y*self.factorWS)) 
                if int(y*self.factorWS) < self.min_val_y:
                    self.min_val_y = int(y*self.factorWS)
                  
        # Determinar la cantidad de filas y columnas
        cant_columnas = max(self.WS_x)+1
        cant_filas = max(self.WS_y) +1

        total_puntos = len(self.WS_x)

        # Colocar el origen del mapa en la esquina inferior izquierda
        for i in range(total_puntos):
            ws_origen_x.append(self.WS_x[i] + abs(self.min_val_x))
            ws_origen_y.append(self.WS_y[i] + abs(self.min_val_y))
        
        cant_columnas += abs(self.min_val_x)
        cant_filas += abs(self.min_val_y)


        # generar la matriz para el espacio de trabajo
        self.mapa_WS= np.zeros((cant_filas,cant_columnas))
        
        for i in range(total_puntos):
            x = ws_origen_x[i]
            y = ws_origen_y[i]
            #print("                  x: ", x, " - y: ",y)
            
            self.mapa_WS[int(y),int(x)] = 1

        #print(self.mapa_WS)
        
    def Mapa_WS_Trayec_2D_3D(self):
        # Actualizar el espacio de trabajo
        self.EspacioTrabajo()
        origin_x = int(-self.min_val_x)#int(-self.min_val_x +self.factorWS*self.T_Exploracion_x[1])
        origin_y = int(-self.min_val_y)#int(-self.min_val_y +self.factorWS*self.T_Exploracion_y[1])
        x = int(-self.min_val_x + self.factorWS*self.x_vehiculo)
        y = int(-self.min_val_y + self.factorWS*self.y_vehiculo)
        self.ruta_optima =Gen_Trayectoria.dijkstra(self.mapa_WS,x,y,origin_x,origin_y)
        
        mapa = self.mapa_WS
        # Obtener las dimensiones del mapa
        #mapa_flip = np.flip(mapa,axis=0)
        filas, columnas = mapa.shape


        # Crear una figura 
        fig = plt.figure()

        ## -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        ## -+-+-+-+-+-+-+-+  Crear subfigura 1 -+-+-+-+-+-+-+-+
        ax1 = fig.add_subplot(121)

        # Configurar límites de los ejes
        ax1.set_xlim(0, columnas)
        ax1.set_ylim(0, filas)

        # Configurar aspecto de los ejes
        ax1.set_aspect('equal')
        ax1.grid(True)

        # Iterar sobre el mapa y graficar obstáculos
        for fila in range(filas):
            for columna in range(columnas):
                if mapa[fila, columna] == 1:
                    # Dibujar obstáculo
                    rect = plt.Rectangle((columna, fila), 1, 1, facecolor='black')
                    ax1.add_patch(rect)

        # Configurar los ejes
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')

        try:
            # Graficar ruta optima
            self.x_rutaOptima = [posicion[1]+0.5 for posicion in self.ruta_optima]
            self.y_rutaOptima = [posicion[0]+0.5 for posicion in self.ruta_optima]
            #plt.plot(inicio[1]+0.5,inicio[0]+0.5,'-o',color='blue')
            
            plt.plot(self.x_rutaOptima, self.y_rutaOptima, '-o', color='green')
            plt.plot(self.x_rutaOptima[0], self.y_rutaOptima[0], '-o', color='blue')
            #plt.plot(self.x_rutaOptima[0],self.y_rutaOptima[0],'o',color = 'red')
            #plt.plot(int(self.factorWS*(self.x_vehiculo))+abs(self.min_val_x),int(self.factorWS*(self.y_vehiculo))+abs(self.min_val_y),'o',color = 'blue')
        except:
            print("No se generó ruta óptima, verificar puntos seleccionados.")    
        
        ## -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        ## -+-+-+-+-+-+-+-+  Crear subfigura 2 -+-+-+-+-+-+-+-+

        ax2 = fig.add_subplot(122, projection='3d')


        # Configurar límites de los ejes
        ax2.set_xlim(0, columnas)
        ax2.set_ylim(0, filas)
        ax2.set_zlim(0, 1)

        # Configurar aspecto de los ejes
        ax2.set_box_aspect([1, 1, 0.1])
        ax2.grid(True)

        # Iterar sobre el mapa y graficar obstáculos
        for fila in range(filas):
            for columna in range(columnas):
                if mapa[fila, columna] == 1:
                    # Dibujar obstáculo como una caja
                    x = columna
                    y = fila
                    z = 0
                    dx = 1
                    dy = 1
                    dz = 1
                    ax2.bar3d(x, y, z, dx, dy, dz, color='black')
        
        try:            
            plt.plot( self.x_rutaOptima,  self.y_rutaOptima, 'o', color='green')
            plt.plot( self.x_rutaOptima[0], self.y_rutaOptima[0],'o',color = 'red')
           
        except:
            print("No se generó ruta óptima, verificar puntos seleccionados.")    
       
        
        # Mostrar la gráfica
        plt.show()
        
    def Mapa_WS_2D_3D(self):
        # Actualizar el espacio de trabajo
        self.EspacioTrabajo()

        
        mapa = self.mapa_WS
        # Obtener las dimensiones del mapa
        #mapa_flip = np.flip(mapa,axis=0)
        filas, columnas = mapa.shape


        # Crear una figura 
        fig = plt.figure()

        ## -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        ## -+-+-+-+-+-+-+-+  Crear subfigura 1 -+-+-+-+-+-+-+-+
        ax1 = fig.add_subplot(121)

        # Configurar límites de los ejes
        ax1.set_xlim(0, columnas)
        ax1.set_ylim(0, filas)

        # Configurar aspecto de los ejes
        ax1.set_aspect('equal')
        ax1.grid(True)

        # Iterar sobre el mapa y graficar obstáculos
        for fila in range(filas):
            for columna in range(columnas):
                if mapa[fila, columna] == 1:
                    # Dibujar obstáculo
                    rect = plt.Rectangle((columna, fila), 1, 1, facecolor='black')
                    ax1.add_patch(rect)
        plt.plot(int(self.factorWS*(self.x_vehiculo)),int(self.factorWS*(self.y_vehiculo)),'o',color = 'red')
        # Configurar los ejes
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')

        ## -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        ## -+-+-+-+-+-+-+-+  Crear subfigura 2 -+-+-+-+-+-+-+-+

        ax2 = fig.add_subplot(122, projection='3d')


        # Configurar límites de los ejes
        ax2.set_xlim(0, columnas)
        ax2.set_ylim(0, filas)
        ax2.set_zlim(0, 1)

        # Configurar aspecto de los ejes
        ax2.set_box_aspect([1, 1, 0.1])
        ax2.grid(True)

        # Iterar sobre el mapa y graficar obstáculos
        for fila in range(filas):
            for columna in range(columnas):
                if mapa[fila, columna] == 1:
                    # Dibujar obstáculo como una caja
                    x = columna
                    y = fila
                    z = 0
                    dx = 1
                    dy = 1
                    dz = 1
                    ax2.bar3d(x, y, z, dx, dy, dz, color='black')

        plt.plot(int(self.factorWS*(self.x_vehiculo)),int(self.factorWS*(self.y_vehiculo)),'o',color = 'red')
        # Mostrar la gráfica
        plt.show()

    def KeyPress_Flag(self):
        if keyboard.is_pressed("m"):
            self.showMap = True
        if keyboard.is_pressed("s"):
            self.showStats = True 
        if keyboard.is_pressed("w"):
            self.show_WS = True 
        if keyboard.is_pressed("1"):
            self.WS_2D_3D = True 
        if keyboard.is_pressed("2"):
            self.WS_Trayec_2D_3D = True   
        if keyboard.is_pressed("3"):
            self.Tray_Control = True

    def Control_pos(self):
        print("Control de pose Init")
        # Acercamiento exponencial
        v0 = 500
        alpha = 50 #%0.5;50
        # PID orientación
        kpO = 15 #15
        kiO = 0.1 
        kdO = 2 #1
        EO = 0
        eO_1 = 0
        eO = 1.0
        eP = 1.0
        
        contador = 0
        #xGoal = [0*self.factorWS]  # mt
        #yGoal = [0*self.factorWS]  # mt
        xGoal = self.x_rutaOptima
        yGoal = self.y_rutaOptima
        while eP >= 0.005 or contador <=len(xGoal):
            self.Odometria()
            self.DatosSensores()
            self.Paredes(self.rotz*180/np.pi)

            #  -*-*-*- posiciones actuales del vehiculo -*-*-*-
            x = (self.factorWS*self.xc[len(self.xc)-1])
            y = (self.factorWS*self.yc[len(self.yc)-1])
            #print("control posición: x: ", x," - y: ", y)
            # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

            # *-*-*-*-*-*-*-* puntos de trayectoria a seguir *-*-*-*-*-*-*-*
            
            # con una trayectoria ya calculada
            if contador < len(xGoal):
                #xg = self.ruta_optima[contador]
                #yg = self.ruta_optima[contador]
                
                if contador == len(xGoal)-1:
                    xg = xGoal[contador]-int(-self.min_val_x)-0.5
                    yg = yGoal[contador]-int(-self.min_val_y)-0.5
                else:
                    xg = xGoal[contador]-int(-self.min_val_x)
                    yg = yGoal[contador]-int(-self.min_val_y)


                coords = [xg,yg]
                #disp(coords)
            

            
            # *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

            #e = [xg-x, yg-y]
            #thetag = np.arctan2(e[1],e[0])
            

            e = [xg - x, yg - y]
            thetag = np.arctan2(e[1], e[0])
            eP = np.linalg.norm(e)
            
            eO = thetag-self.rotz
            eO = np.arctan2(np.sin(eO),np.cos(eO))
            
            
            if eO >0:
                flag_dGiro = True  # bandera dirección del giro, 
                                    # True = sentido horario
                                    # False = sentido antihorario
            else:
                flag_dGiro = False

            eO = abs(eO)

            # Control de velocidad lineal
            #kP = v0 * (1-np.exp(-alpha*eP**2)) / eP
            kP = 1
            v = abs(kP*eP)

            # Control de velocidad angular
            eO_D = eO - eO_1
            EO = EO + eO
            w = kpO*eO + kiO*EO + kdO*eO_D
            eO_1 = eO

            self.left_motor.setVelocity(0)
            self.right_motor.setVelocity(0)
            if eO >=0.03:
                if flag_dGiro == True:
                    giroder = (w*self.distanceCenter)/self.wheelRadius
                    giroiz = (-w*self.distanceCenter)/self.wheelRadius
                else: 
                    giroder = (-w*self.distanceCenter)/self.wheelRadius
                    giroiz = (w*self.distanceCenter)/self.wheelRadius

                
                if giroder >= 0.5:
                    giroder = 0.5
                    giroiz = -0.5
                elif giroder <= -0.5:
                    giroder = -0.5
                    giroiz = 0.5
                
             
                
                self.right_motor.setVelocity(giroder)
                self.left_motor.setVelocity(giroiz)

            elif eP > 0.2:
                if v > 4:
                    v = 4
                self.left_motor.setVelocity(v)
                self.right_motor.setVelocity(v)
            else: 
                contador += 1
                
                
            if self.step(self.timestep) == -1:
                break
        
        while not(keyboard.is_pressed("c")):
            None

    def Odometria(self):
        #print("Funcion de odometria")
        #self.DatosSensores()

        theta_d = (self.PS_Right_value - self.PS_Right_Anterior)*1.003
        theta_i = (self.PS_Left_value - self.PS_Left_Anterior)*1.003
               
        self.phi += (self.wheelRadius*theta_d-self.wheelRadius*theta_i)/(2*self.distanceCenter)*(180/np.pi)
        
        
        dPromedio = (self.wheelRadius*theta_d+self.wheelRadius*theta_i)/2
        self.xc.append(self.xc[len(self.xc)-1] +(dPromedio)*np.cos(self.phi*np.pi/180))
        self.yc.append(self.yc[len(self.yc)-1] +(dPromedio)*np.sin(self.phi*np.pi/180))
       

        self.PS_Right_Anterior = self.PS_Right_value # posicion de la rueda derecha
        self.PS_Left_Anterior  = self.PS_Left_value # posicion de la rueda izquierda
        
        #print("xc: ", self.xc[len(self.xc)-1], " - yc: ",self.yc[len(self.yc)-1],"   ----   xVehiculo: ",self.x_vehiculo," - yVehiculo: ",self.y_vehiculo, "\n|| phi: ", self.phi," - rotz", self.angulo)
        #print('theta_d: ',theta_d,' - theta_i: ',theta_i)
        
controller = Slave()
controller.run()

