import numpy as np
import keyboard

import Rot_Control
import Odometria
import Obstaculos

def Rutina_Inicio(agente):
    for i in [45,45,45,45,45,45,45,45]:
        agente.angulo += i
        Rot_Control.Rot_Control(agente.angulo,agente)

def Explorar(agente):
    coef_velocidad = 0.01
    vel_max = 8
    ds0_min_val = 30
    dMin = 15.5#agente.distanceCenter*100#15.5
    cont = 0
    agente.FrenoEmergencia = False
    while (agente.ds0_value >= agente.ds2_value) and (agente.ds0_value >= agente.ds4_value) or agente.ds0_value>ds0_min_val:
        #agente.DatosSensores()
        
        Odometria.Avance_Lineal(agente,0) # Inicio de avance lineal

        agente.left_motor.setVelocity(vel_max*coef_velocidad)
        agente.right_motor.setVelocity(vel_max*coef_velocidad)

        if coef_velocidad < 1:
            coef_velocidad += 0.05

        agente.DatosSensores()
        Odometria.Avance_Lineal(agente,1) # Fin de avance lineal
        Odometria.Odometria(agente)
        Obstaculos.Obstaculos(agente,agente.rotz*180/np.pi)

        if agente.ds2_value < 100 and agente.ds4_value < 100:
            ds0_min_val = 30
        else:
            ds0_min_val = 100

        if cont == 9:
            #Rot_Control.Rot_Control(agente.angulo,agente)
            cont = 0
        cont +=1        
        
        # Condiciones especiales para cambiar la rotación
        if agente.ds0_value <= dMin or agente.ds1_value <= dMin or agente.ds5_value <= dMin:
            print("---- Freno de emergencia ----")
            agente.FrenoEmergencia = True
            
            Odometria.Avance_Lineal(agente,0) # Inicio de avance lineal
            while coef_velocidad > 0.1:
                
                agente.left_motor.setVelocity(vel_max*coef_velocidad)
                agente.right_motor.setVelocity(vel_max*coef_velocidad)
                #Odometria.Odometria(agente)

                coef_velocidad -= 0.5
            
            agente.left_motor.setVelocity(0)
            agente.right_motor.setVelocity(0)
            #Odometria.Odometria(agente)
            agente.DatosSensores()
            Odometria.Avance_Lineal(agente,1) # Fin de avance lineal
            Odometria.Odometria(agente)
            Obstaculos.Obstaculos(agente,agente.rotz*180/np.pi)
            break                   
        
        if agente.step(agente.timestep) == -1:
            break
    
    if agente.FrenoEmergencia == False:
        Odometria.Avance_Lineal(agente,0) # Inicio de avance lineal
        while coef_velocidad > 0.1:
            agente.left_motor.setVelocity(vel_max*coef_velocidad)
            agente.right_motor.setVelocity(vel_max*coef_velocidad)
            #Odometria.Odometria(agente)
            
            coef_velocidad -= 0.1
            if agente.step(agente.timestep) == -1:
                break
        agente.left_motor.setVelocity(0)
        agente.right_motor.setVelocity(0)
        
        agente.DatosSensores()
        Odometria.Avance_Lineal(agente,1) # Fin de avance lineal
        Odometria.Odometria(agente)
        Obstaculos.Obstaculos(agente,agente.rotz*180/np.pi)

        #Odometria.Odometria(agente)

def Seguimiento_Trayectoria(agente):
    # Función para seguimiento de trayectoria óptima
    print("Seguimiento de trayectoria óptima")

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
    #xGoal = [0*agente.factorWS]  # mt
    #yGoal = [0*agente.factorWS]  # mt

    xGoal = [posicion[1]+0.5 for posicion in agente.ruta_optima]
    yGoal = [posicion[0]+0.5 for posicion in agente.ruta_optima]

    while eP >= 0.005 or contador <=len(xGoal):
        Odometria.Odometria(agente)
        agente.DatosSensores()
        #agente.Paredes(agente.rotz*180/np.pi)

        #  -*-*-*- posiciones actuales del vehiculo -*-*-*-
        x = (agente.factorWS*agente.xc[len(agente.xc)-1])
        y = (agente.factorWS*agente.yc[len(agente.yc)-1])
        #print("control posición: x: ", x," - y: ", y)
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

        # *-*-*-*-*-*-*-* puntos de trayectoria a seguir *-*-*-*-*-*-*-*
        
        # con una trayectoria ya calculada
        if contador < len(xGoal):
            #xg = agente.ruta_optima[contador]
            #yg = agente.ruta_optima[contador]
            
            if contador == len(xGoal)-1:
                xg = xGoal[contador]-int(-agente.min_val_x)-0.5
                yg = yGoal[contador]-int(-agente.min_val_y)-0.5
            else:
                xg = xGoal[contador]-int(-agente.min_val_x)
                yg = yGoal[contador]-int(-agente.min_val_y)


            coords = [xg,yg]
            #disp(coords)
        

        
        # *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

        #e = [xg-x, yg-y]
        #thetag = np.arctan2(e[1],e[0])
        

        e = [xg - x, yg - y]
        thetag = np.arctan2(e[1], e[0])
        eP = np.linalg.norm(e)
        
        eO = thetag-agente.rotz
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

        agente.left_motor.setVelocity(0)
        agente.right_motor.setVelocity(0)
        if eO >=0.03:
            if flag_dGiro == True:
                giroder = (w*agente.distanceCenter)/agente.wheelRadius
                giroiz = (-w*agente.distanceCenter)/agente.wheelRadius
            else: 
                giroder = (-w*agente.distanceCenter)/agente.wheelRadius
                giroiz = (w*agente.distanceCenter)/agente.wheelRadius

            
            if giroder >= 0.5:
                giroder = 0.5
                giroiz = -0.5
            elif giroder <= -0.5:
                giroder = -0.5
                giroiz = 0.5
            
            
            
            agente.right_motor.setVelocity(giroder)
            agente.left_motor.setVelocity(giroiz)

        elif eP > 0.2:
            if v > 4:
                v = 4
            agente.left_motor.setVelocity(v)
            agente.right_motor.setVelocity(v)
        else: 
            contador += 1
            
            
        if agente.step(agente.timestep) == -1:
            break
    