import numpy as np


def Odometria_Init(agente):
    agente.DatosSensores()
    # variables de odometría 
    agente.PS_Right_Anterior = agente.PS_Right_value  # Pocisión de rueda derecha en n-1
    agente.PS_Left_Anterior  = agente.PS_Left_value   # Pocisión de rueda izquierda en n-1



def Odometria(agente):
    #print("Funcion de odometria")
    #agente.DatosSensores()
    
    theta_d = (agente.PS_Right_value - agente.PS_Right_Anterior)
    theta_i = (agente.PS_Left_value - agente.PS_Left_Anterior)
           
    agente.phi += (agente.wheelRadius*theta_d-agente.wheelRadius*theta_i)/(agente.distanceCenter)*(180/np.pi)
        
    dPromedio = (agente.wheelRadius*theta_d+agente.wheelRadius*theta_i)/2
    agente.xc.append(agente.xc[len(agente.xc)-1] +(dPromedio)*np.cos(agente.phi*np.pi/180))
    agente.yc.append(agente.yc[len(agente.yc)-1] +(dPromedio)*np.sin(agente.phi*np.pi/180))

    agente.PS_Right_Anterior = agente.PS_Right_value # posicion de la rueda derecha
    agente.PS_Left_Anterior  = agente.PS_Left_value # posicion de la rueda izquierda
    
    #print(dPromedio)
    
    #print("xc: ", agente.xc[len(agente.xc)-1], " - yc: ",agente.yc[len(agente.yc)-1])
    #print('theta_d: ',theta_d,' - theta_i: ',theta_i)
    #print(round(agente.phi,0), "  --  ", agente.angulo)



def Avance_Lineal(agente,estado):
    # estado: 0 para inicio de medición
    # 1 para fin de medión y obtener resultado
    
    agente.DatosSensores()
    if estado == 0:
         # variables de odometría lineal
        agente.distAnterior_Right = agente.DRW_Right
        agente.distAnterior_Left = agente.DRW_Left
        
    elif estado == 1:
        # llanta derecha
        agente.distActual_Right = agente.DRW_Right
        agente.d_lineaRecta_Right = agente.distActual_Right-agente.distAnterior_Right
        
        # llanta izquierda
        agente.distActual_Left = agente.DRW_Left
        agente.d_lineaRecta_Left = agente.distActual_Left-agente.distAnterior_Left
        
        agente.promedio_distancia_trayecto = (agente.d_lineaRecta_Left+agente.d_lineaRecta_Right)/2
        agente.Distancias_lineaRecta.append(agente.promedio_distancia_trayecto)
        agente.Angulos.append(agente.angulo)