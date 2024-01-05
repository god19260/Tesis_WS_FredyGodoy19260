import numpy as np


def Obstaculos(agente, angulo):
    inflate = 4
    #print(len(agente.T_Exploracion_x) , " -- ",len(agente.T_Exploracion_y) , " -- " ,len(agente.Pared_x) , " -- ",len(agente.Pared_y))
    if agente.ds0_value<agente.rango_max_dsen:
        x = (agente.ds0_value-inflate)*np.cos((angulo)*np.pi/180)/100
        y = (agente.ds0_value-inflate)*np.sin((angulo)*np.pi/180)/100
        
        agente.Pared_x_ds0.append(agente.T_Exploracion_x[-1]+x)
        agente.Pared_y_ds0.append(agente.T_Exploracion_y[-1]+y)

    if agente.ds2_value<agente.rango_max_dsen:
        x = (agente.ds2_value-inflate)*np.cos((angulo-90)*np.pi/180)/100
        y = (agente.ds2_value-inflate)*np.sin((angulo-90)*np.pi/180)/100
        
        agente.Pared_x_ds2.append(agente.T_Exploracion_x[-1]+x)
        agente.Pared_y_ds2.append(agente.T_Exploracion_y[-1]+y)
    
    if agente.ds4_value<agente.rango_max_dsen:
        x = (agente.ds4_value-inflate)*np.cos((angulo+90)*np.pi/180)/100
        y = (agente.ds4_value-inflate)*np.sin((angulo+90)*np.pi/180)/100
        
        agente.Pared_x_ds4.append(agente.T_Exploracion_x[-1]+x)
        agente.Pared_y_ds4.append(agente.T_Exploracion_y[-1]+y)
    
    if agente.ds1_value<agente.rango_max_dsen:
        x = (agente.ds1_value-inflate)*np.cos((angulo-45)*np.pi/180)/100
        y = (agente.ds1_value-inflate)*np.sin((angulo-45)*np.pi/180)/100
        
        agente.Pared_x_ds1.append(agente.T_Exploracion_x[-1]+x)
        agente.Pared_y_ds1.append(agente.T_Exploracion_y[-1]+y)
    
    if agente.ds5_value<agente.rango_max_dsen:
        x = (agente.ds5_value-inflate)*np.cos((angulo+45)*np.pi/180)/100
        y = (agente.ds5_value-inflate)*np.sin((angulo+45)*np.pi/180)/100
        
        agente.Pared_x_ds5.append(agente.T_Exploracion_x[-1]+x)
        agente.Pared_y_ds5.append(agente.T_Exploracion_y[-1]+y)

def Espacio_Trabajo(agente,modo):
    #print(" *-*-*-*-*-* Determinar espacio de trabajo *-*-*-*-*-*")
    if modo == 0:
        cant_columnas = 0
        cant_filas = 0

        
        d_sensors = [[agente.Pared_x_ds0,agente.Pared_y_ds0],
                        [agente.Pared_x_ds4,agente.Pared_y_ds4],
                        [agente.Pared_x_ds2,agente.Pared_y_ds2]]#,
                        
                        
                        
                        #[agente.Pared_x_ds5,agente.Pared_y_ds5],
                        #[agente.Pared_x_ds5,agente.Pared_y_ds5]
                        #]
        

        # preparar arrays para el espacio de trabajo
        agente.WS_x.clear()
        agente.WS_y.clear()
        ws_origen_x, ws_origen_y = [],[]

        for d_sensor in d_sensors:
            x_ds = d_sensor[0] # x de distance sensor 
            y_ds = d_sensor[1] # y de distance sensor 

            for x in x_ds:
                agente.WS_x.append(int(x*agente.factorWS))
                if int(x*agente.factorWS) < agente.min_val_x:
                    agente.min_val_x = int(x*agente.factorWS)

            for y in y_ds:
                agente.WS_y.append(int(y*agente.factorWS)) 
                if int(y*agente.factorWS) < agente.min_val_y:
                    agente.min_val_y = int(y*agente.factorWS)
                    
        # Determinar la cantidad de filas y columnas
        cant_columnas = max(agente.WS_x)+1
        cant_filas = max(agente.WS_y) +1

        total_puntos = len(agente.WS_x)

        # Colocar el origen del mapa en la esquina inferior izquierda
        for i in range(total_puntos):
            ws_origen_x.append(agente.WS_x[i] + abs(agente.min_val_x))
            ws_origen_y.append(agente.WS_y[i] + abs(agente.min_val_y))
        
        cant_columnas += abs(agente.min_val_x)
        cant_filas += abs(agente.min_val_y)


        # generar la matriz para el espacio de trabajo
        agente.mapa_WS= np.zeros((cant_filas,cant_columnas))
        
        for i in range(total_puntos):
            x = ws_origen_x[i]
            y = ws_origen_y[i]
            #print("                  x: ", x, " - y: ",y)
            
            agente.mapa_WS[int(y),int(x)] = 1

    elif modo == 1:
        cant_columnas = 0
        cant_filas = 0

        
        d_sensors = [[agente.puntos_mapa_x,agente.puntos_mapa_y]]#,
                        
                        
                        
                        #[agente.Pared_x_ds5,agente.Pared_y_ds5],
                        #[agente.Pared_x_ds5,agente.Pared_y_ds5]
                        #]
        

        # preparar arrays para el espacio de trabajo
        agente.WS_x.clear()
        agente.WS_y.clear()
        ws_origen_x, ws_origen_y = [],[]

        for d_sensor in d_sensors:
            x_ds = d_sensor[0] # x de distance sensor 
            y_ds = d_sensor[1] # y de distance sensor 

            for x in x_ds:
                agente.WS_x.append(int(x*agente.factorWS))
                if int(x*agente.factorWS) < agente.min_val_x:
                    agente.min_val_x = int(x*agente.factorWS)

            for y in y_ds:
                agente.WS_y.append(int(y*agente.factorWS)) 
                if int(y*agente.factorWS) < agente.min_val_y:
                    agente.min_val_y = int(y*agente.factorWS)
                    
        # Determinar la cantidad de filas y columnas
        cant_columnas = max(agente.WS_x)+1
        cant_filas = max(agente.WS_y) +1

        total_puntos = len(agente.WS_x)

        # Colocar el origen del mapa en la esquina inferior izquierda
        for i in range(total_puntos):
            ws_origen_x.append(agente.WS_x[i] + abs(agente.min_val_x))
            ws_origen_y.append(agente.WS_y[i] + abs(agente.min_val_y))
        
        cant_columnas += abs(agente.min_val_x)
        cant_filas += abs(agente.min_val_y)


        # generar la matriz para el espacio de trabajo
        agente.mapa_WS= np.zeros((cant_filas,cant_columnas))
        
        for i in range(total_puntos):
            x = ws_origen_x[i]
            y = ws_origen_y[i]
            #print("                  x: ", x, " - y: ",y)
            
            agente.mapa_WS[int(y),int(x)] = 1



        