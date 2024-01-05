
from controller import Robot, Emitter, Receiver
import numpy as np
import math



# Funciones Desarrolladas en este trabajo
import Rot_Control
import Explorar
import Condiciones_Giro
import Odometria
import Graficas
import Obstaculos
import Trayectoria

class Slave(Robot):
    # get the time step of the current world.
    timestep = 3
    
    # Especificaciones del mundo
    size_x = 5.0 #m
    size_y = 5.0 #m

    #------------------ Características del robot ------------------
    wheelRadius = 0.035 #radio en m 
    distanceCenter = 0.0748664*2 #0.075 # distancia en m 
    angulo = 90  # ángulo respecto marco de referencia entorno
    
    #--------------------------------------------------------------- 
    
    
    #-------------------------- Odometría -------------------------- 

    PS_Right_Anterior = 0  # Pocisión de rueda derecha en n-1
    PS_Left_Anterior  = 0  # Pocisión de rueda izquierda en n-1

    phi = angulo # rotz estimado respecto marco de referencia entorno

    # posición centroide vehículo
    xc = [0]
    yc = [0]

    # Distancia en tramos de linea recta
    Distancias_lineaRecta = []
    Angulos = []
    Distancia_Total = 0
    T_Exploracion_x = [0]
    T_Exploracion_y = [0]
    T_Exploracion_GPS_x = []
    T_Exploracion_GPS_y = []
    error_GPS_Estimado = []
    #---------------------------------------------------------------  

    #------------------------- Obstaculos --------------------------
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

    # Espacio de trabajo
    factorWS = 10 # cada recuadro del mapa es de dimensiones (factor x factor)
    WS_x = []
    WS_y = []
    min_val_x = 0
    min_val_y = 0
    
    #---------------------------------------------------------------

    #------------------------- Trayectoria -------------------------
    ruta_optima = []
    objetivo_x = 0
    objetivo_y = 0
    #---------------------------------------------------------------


    #--------------------- Definiciones previas --------------------
    distanceSensors = []
    #---------------------------------------------------------------  


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

    
    def DatosSensores_Init(self):
        self.PS_Right_StartValue =  self.PositionSensor_right.getValue()  # PS_Right_value --> position sensor right value
        self.PS_Left_StartValue  =  self.PositionSensor_left.getValue()  # PS_Right_value --> position sensor right value

        # Offset para valores GPS 
        # Actualizar valores de GPS
        self.GPS_values = self.GPS.getValues()
        self.T_Exploracion_GPS_x.append(self.GPS_values[0]+self.size_x/2)
        self.T_Exploracion_GPS_y.append(self.GPS_values[1]+self.size_y/2)

        self.delta_GPS_Estimado_x = abs(self.T_Exploracion_GPS_x[0])
        self.delta_GPS_Estimado_y = abs(self.T_Exploracion_GPS_y[0])


    def DatosSensores(self):
        # Actualizar sensores de distancia
        self.ds0_value = self.distanceSensors[0].getValue()+8
        self.ds1_value = self.distanceSensors[1].getValue()+8
        self.ds2_value = self.distanceSensors[2].getValue()+8
        self.ds3_value = self.distanceSensors[3].getValue()+8
        self.ds4_value = self.distanceSensors[4].getValue()+8
        self.ds5_value = self.distanceSensors[5].getValue()+8

        # Actualizar sensor de compass y angulo de rotz
        self.compass_values = self.compass.getValues()
        radian = np.arctan2(self.compass_values[0],self.compass_values[1])
        self.rotz_g = radian*180/np.pi     # Rotación en el eje z del vehículo en grados
        self.rotz = radian                 # Rotación en el eje z del vehículo en radianes

        # Actualizar valores de sensores de posición de las ruedas
        self.PS_Right_value = self.PositionSensor_right.getValue()- self.PS_Right_StartValue   # PS_Right_value --> position sensor right value
        self.PS_Left_value  = self.PositionSensor_left.getValue()- self.PS_Left_StartValue    # PS_Left_value --> position sensor left value 
        
        # Actualizar valores de GPS
        self.GPS_values = self.GPS.getValues()
        

Agente_1 = Slave()

# Configuración de emisor
emitter = Agente_1.getDevice("emitter")
emitter.setChannel(1)

# Configuración de receptor
receiver = Agente_1.getDevice("receiver")
receiver.enable(Agente_1.timestep)

if Agente_1.step(Agente_1.timestep) != -1:
    None


Agente_1.DatosSensores_Init() 
Agente_1.DatosSensores()

# inicializar el ángulo de rotación del vehículo
Agente_1.angulo = Agente_1.rotz_g
Agente_1.phi = Agente_1.angulo

Odometria.Odometria_Init(Agente_1)

Explorar.Rutina_Inicio(Agente_1)

tiempos = [8] # minutos4n
u = 0
while Agente_1.step(Agente_1.timestep) != -1:
    Agente_1.DatosSensores()
    Rot_Control.Rot_Control(Agente_1.angulo,Agente_1)
    Explorar.Explorar(Agente_1)
    
    

    if Agente_1.getTime() >= tiempos[u]*60:
        #------ Enviar datos a supervisor ----
        data = "Robot: Hola"
        """
        T_Exploracion_x_str = ' '.join(map(str, Agente_1.Pared_x_ds0))
        T_Exploracion_y_str = ' '.join(map(str, Agente_1.Pared_y_ds0))  
        
        T_Exploracion_x_str =T_Exploracion_x_str+' '+ ' '.join(map(str, Agente_1.Pared_x_ds1))
        T_Exploracion_y_str =T_Exploracion_y_str+' '+ ' '.join(map(str, Agente_1.Pared_y_ds1))  
        
        T_Exploracion_x_str =T_Exploracion_x_str+' '+ ' '.join(map(str, Agente_1.Pared_x_ds2))
        T_Exploracion_y_str =T_Exploracion_y_str+' '+ ' '.join(map(str, Agente_1.Pared_y_ds2))

        T_Exploracion_x_str =T_Exploracion_x_str+' '+ ' '.join(map(str, Agente_1.Pared_x_ds3))
        T_Exploracion_y_str =T_Exploracion_y_str+' '+ ' '.join(map(str, Agente_1.Pared_y_ds3))

        T_Exploracion_x_str =T_Exploracion_x_str+' '+ ' '.join(map(str, Agente_1.Pared_x_ds4))
        T_Exploracion_y_str =T_Exploracion_y_str+' '+ ' '.join(map(str, Agente_1.Pared_y_ds4))

        T_Exploracion_x_str =T_Exploracion_x_str+' '+ ' '.join(map(str, Agente_1.Pared_x_ds5))
        T_Exploracion_y_str =T_Exploracion_y_str+' '+ ' '.join(map(str, Agente_1.Pared_y_ds5))

        desfase_x =  str(Agente_1.T_Exploracion_GPS_x[0])
        desfase_y =  str(Agente_1.T_Exploracion_GPS_y[0])

        print("cantidad de puntos (controlador de vehiculo): ", len(Agente_1.Pared_x_ds0),"  ",len(Agente_1.Pared_x_ds0)*2)
        data =   desfase_x+ ' ' +desfase_y+ ' ' + T_Exploracion_x_str + ' '+ T_Exploracion_y_str
        """
        emitter.send(data.encode())
        
        datos_obtenidos = False
        while datos_obtenidos == False:
            # ----- Recibir datos de supervisor -----
            if receiver.getQueueLength() > 0:
                data = receiver.getString()
                print(data)
                receiver.nextPacket()
                numeros = eval(data)
                print("tipo de dato de data en controlador: ", type(data))
                try:
                    # Asignar los valores a variables individuales
                    primer_numero = float(numeros[0])
                    segundo_numero = float(numeros[1])
                    datos_obtenidos = True
                except:
                    None
            
            if Agente_1.step(Agente_1.timestep) == -1:
                break
        
        # Se considera este espacio el fin de la exploración
        # y se genera la trayectoria al punto de inicio
        Obstaculos.Espacio_Trabajo(Agente_1)
        Agente_1.objetivo_x = (primer_numero+Agente_1.size_x/2.0)*Agente_1.factorWS-Agente_1.T_Exploracion_GPS_x[0]
        Agente_1.objetivo_y = (segundo_numero+Agente_1.size_y/2.0)*Agente_1.factorWS-Agente_1.T_Exploracion_GPS_y[0]

        Trayectoria.Ruta_Optima(Agente_1, Agente_1.objetivo_x, Agente_1.objetivo_y)

        Graficas.graph_select(Agente_1)

        if u == 0:
            Explorar.Seguimiento_Trayectoria(Agente_1)

        u += 1
        try:
            tiempos[u] = tiempos[u]+Agente_1.getTime()/60
        except:
            print("Tiempo de Simulación alcanzado.")
            break

    Condiciones_Giro.DecisionGiro(Agente_1)

    if Agente_1.step(Agente_1.timestep) == -1:
        break
    



