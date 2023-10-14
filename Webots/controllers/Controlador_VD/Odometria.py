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
    # Función de odometría unica solo para trayectoria de exploración
    
    # estado: 0 para inicio de medición
    # 1 para fin de medión y obtener resultado
    
    #agente.DatosSensores()
    if estado == 0:
        agente.revsRight = agente.PS_Right_value/(2*np.pi)
        agente.revsLeft  = agente.PS_Left_value/(2*np.pi)
        
        agente.DRW_Right =  agente.revsRight*2*np.pi*agente.wheelRadius    # Distancia recorrida por la llanta derecha
        agente.DRW_Left  =  agente.revsLeft*2*np.pi*agente.wheelRadius     # Distancia recorrida por la llanta izquierda


         # variables de odometría lineal
        agente.distAnterior_Right = agente.DRW_Right
        agente.distAnterior_Left = agente.DRW_Left
        #print("Inicio lineal:  ", agente.distAnterior_Right)
        
    if estado == 1:
        agente.revsRight = agente.PS_Right_value/(2*np.pi)
        agente.revsLeft  = agente.PS_Left_value/(2*np.pi)
        
        agente.DRW_Right =  agente.revsRight*2*np.pi*agente.wheelRadius    # Distancia recorrida por la llanta derecha
        agente.DRW_Left  =  agente.revsLeft*2*np.pi*agente.wheelRadius     # Distancia recorrida por la llanta izquierda



        # llanta derecha
        agente.distActual_Right = agente.DRW_Right
        agente.d_lineaRecta_Right = agente.distActual_Right-agente.distAnterior_Right
        
        # llanta izquierda
        agente.distActual_Left = agente.DRW_Left
        agente.d_lineaRecta_Left = agente.distActual_Left-agente.distAnterior_Left
        
        agente.promedio_distancia_trayecto = (agente.d_lineaRecta_Left+agente.d_lineaRecta_Right)/2
        agente.Distancia_Total += agente.promedio_distancia_trayecto
        agente.Distancias_lineaRecta.append(agente.promedio_distancia_trayecto)
        agente.Angulos.append(agente.angulo)
        

        # Odometría. Posición estimada trayectoria de exploración 
        agente.x_vehiculo = agente.T_Exploracion_x[-1]+np.cos(agente.angulo*np.pi/180)*agente.promedio_distancia_trayecto
        agente.y_vehiculo = agente.T_Exploracion_y[-1]+np.sin(agente.angulo*np.pi/180)*agente.promedio_distancia_trayecto

        agente.T_Exploracion_x.append(agente.x_vehiculo) # Trayectoria exploración coordenada en x
        agente.T_Exploracion_y.append(agente.y_vehiculo) # Trayectoria exploración coordenada en y 

        # Odometría. Posición trayectoria exploración obtenida con GPS
        agente.T_Exploracion_GPS_x.append(agente.GPS_values[0]+agente.size_x/2)
        agente.T_Exploracion_GPS_y.append(agente.GPS_values[1]+agente.size_y/2)
        
        # Obtener el % de error entre el posición estimada y el obtenido con GPS
        v_estimado = np.sqrt((agente.T_Exploracion_x[-1]+agente.delta_GPS_Estimado_x)**2+(agente.T_Exploracion_y[-1]+agente.delta_GPS_Estimado_y)**2)
        v_real = np.sqrt(agente.T_Exploracion_GPS_x[-1]**2 +agente.T_Exploracion_GPS_y[-1]**2)
        #v_aproximado = round(agente.y_vehiculo+agente.delta_GPS_revs_y,4)
        #v_real = round(agente.GPS_values[1]+agente.size_y/2,4) 

        agente.error_GPS_Estimado.append(abs((v_estimado-v_real)/abs(v_real))*100)
        #print(agente.GPS_values[0]+agente.size_x/2," -- ",agente.GPS_values[1]+agente.size_y/2," || ",agente.x_vehiculo+agente.delta_GPS_revs_x," -- ",agente.y_vehiculo+agente.delta_GPS_revs_y)
        
        
        #print("Fin de lineal:  ", agente.distActual_Right)
        #print(" ")
        #print(agente.distActual_Right, "  -  ", agente.distAnterior_Right  )