import numpy as np

# Función Controlador de rotación

# Parámetros: 
# rotz goal en grados

def Rot_Control(rotz_goal,agente):
    # PID orientación
    kpO = 15 #15
    kiO = 0.001 
    kdO = 1 #1
    EO = 0
    eO_1 = 0
    eO = 1.0

    while eO > 0.003:
        agente.DatosSensores()
        x = 0.5
        y = 0.5
        #e = [xg-x, yg-y]
        #thetag = np.arctan2(e[1],e[0])
        thetag = rotz_goal/180*np.pi
        eO = thetag-agente.rotz
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
                giroder = (w*agente.distanceCenter)/agente.wheelRadius
                giroiz = -(w*agente.distanceCenter)/agente.wheelRadius
            else: 
                giroder = -(w*agente.distanceCenter)/agente.wheelRadius
                giroiz = (w*agente.distanceCenter)/agente.wheelRadius

            if giroder >= 5:
                giroder = 5
                giroiz = -5
            elif giroder <= -5:
                giroder = -5
                giroiz = 5
            
            """
            if giroiz >= 0.5:
                giroiz = 0.5
            elif giroiz <= -0.5:
                giroiz = -0.5
            """

            agente.right_motor.setVelocity(giroder)
            agente.left_motor.setVelocity(giroiz)
        
        else:
            agente.left_motor.setVelocity(0)
            agente.right_motor.setVelocity(0)

        if agente.step(agente.timestep) == -1:
            break