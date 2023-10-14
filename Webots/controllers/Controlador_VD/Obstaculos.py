import numpy as np


def Obstaculos(agente, angulo):

    #print(len(agente.T_Exploracion_x) , " -- ",len(agente.T_Exploracion_y) , " -- " ,len(agente.Pared_x) , " -- ",len(agente.Pared_y))
    if agente.ds0_value<agente.rango_max_dsen:
        x = agente.ds0_value*np.cos((angulo)*np.pi/180)/100
        y = agente.ds0_value*np.sin((angulo)*np.pi/180)/100
        
        agente.Pared_x_ds0.append(agente.T_Exploracion_x[-1]+x)
        agente.Pared_y_ds0.append(agente.T_Exploracion_y[-1]+y)

    if agente.ds2_value<agente.rango_max_dsen:
        x = agente.ds2_value*np.cos((angulo-90)*np.pi/180)/100
        y = agente.ds2_value*np.sin((angulo-90)*np.pi/180)/100
        
        agente.Pared_x_ds2.append(agente.T_Exploracion_x[-1]+x)
        agente.Pared_y_ds2.append(agente.T_Exploracion_y[-1]+y)
    
    if agente.ds4_value<agente.rango_max_dsen:
        x = agente.ds4_value*np.cos((angulo+90)*np.pi/180)/100
        y = agente.ds4_value*np.sin((angulo+90)*np.pi/180)/100
        
        agente.Pared_x_ds4.append(agente.T_Exploracion_x[-1]+x)
        agente.Pared_y_ds4.append(agente.T_Exploracion_y[-1]+y)
    
    if agente.ds1_value<agente.rango_max_dsen:
        x = agente.ds1_value*np.cos((angulo-45)*np.pi/180)/100
        y = agente.ds1_value*np.sin((angulo-45)*np.pi/180)/100
        
        agente.Pared_x_ds1.append(agente.T_Exploracion_x[-1]+x)
        agente.Pared_y_ds1.append(agente.T_Exploracion_y[-1]+y)
    
    if agente.ds5_value<agente.rango_max_dsen:
        x = agente.ds5_value*np.cos((angulo+45)*np.pi/180)/100
        y = agente.ds5_value*np.sin((angulo+45)*np.pi/180)/100
        
        agente.Pared_x_ds5.append(agente.T_Exploracion_x[-1]+x)
        agente.Pared_y_ds5.append(agente.T_Exploracion_y[-1]+y)
