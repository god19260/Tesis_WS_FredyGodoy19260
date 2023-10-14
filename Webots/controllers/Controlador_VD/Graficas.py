import matplotlib.pyplot as plt

def Trayectoria_Exploracion(agente):
     # Crear una figura 
    agente.fig = plt.figure()
    agente.fig.suptitle('Trayectoria Exploración')
    
    # *-*-*-*-*-*-*-*-*-*-*-*-* Crear una subfigura *-*-*-*-*-*-*-*-*-*-*-*-*   
    # (Trayectoria experimental, obtenida de las revoluciones de las ruedas)
    agente.ax1 = agente.fig.add_subplot(121)

    # Configurar límites de los ejes
    agente.ax1.set_xlim(0, agente.size_x*10)
    agente.ax1.set_ylim(0, agente.size_y*10)

    # Configurar aspecto de los ejes
    agente.ax1.set_aspect('equal')
    agente.ax1.grid(True)
    
    
    plt.plot(agente.T_Exploracion_x, agente.T_Exploracion_y, '-o', color='red')
    #plt.plot(agente.Pared_x_ds2,agente.Pared_y_ds2,'o', color='black')
    #plt.plot(agente.Pared_x_ds4,agente.Pared_y_ds4,'o', color='black')
    #plt.plot(agente.Pared_x_ds0,agente.Pared_y_ds0,'o', color='black')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Por posición de ruedas')
    plt.xlim(0,5)
    plt.ylim(0,5)
    plt.grid(True)

    
    # *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*- 
    # *-*-*-*-*-*-*-*-*-*-*-*-* Crear otra subfigura *-*-*-*-*-*-*-*-*-*-*-*-*   
    #            (Trayectoria Teórica, obtenida por el GPS del robot)
    agente.ax2 = agente.fig.add_subplot(122)

    # Configurar límites de los ejes
    agente.ax2.set_xlim(0, agente.size_x*10)
    agente.ax2.set_ylim(0, agente.size_y*10)

    # Configurar aspecto de los ejes
    agente.ax2.set_aspect('equal')
    agente.ax2.grid(True)
    
    plt.plot(agente.T_Exploracion_GPS_x, agente.T_Exploracion_GPS_y, '-o', color='green')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('GPS')
    plt.xlim(0,5)
    plt.ylim(0,5)
    plt.grid(True)
    
    # *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*- 
    # *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*- 
    plt.show()
def Error(agente):
    # ------------------------- Crear una figura -------------------------- 
    # */*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
    # */*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
    agente.fig2 = plt.figure()
    agente.fig2.suptitle('Errores y coordenadas')
    # */*/*/*/*/*/*/*/*/*/*/*/* Crear una subfigura */*/*/*/*/*/*/*/*/*/*/*
    agente.ax1_fig2 = agente.fig2.add_subplot(111)

    # Configurar límites de los ejes
    agente.ax1_fig2.set_xlim(0,len(agente.T_Exploracion_GPS_x))
    agente.ax1_fig2.set_ylim(0,100)

    # Configurar aspecto de los ejes
    
    agente.ax1_fig2.grid(True)
    
    plt.title('Error acumulado')
    plt.plot(agente.error_GPS_Estimado, color='blue')
    plt.xlabel('no. de nodos')
    plt.ylabel('Porcentaje de error')  
        
    plt.show()

def Obstaculos(agente):
     # Crear una figura 
    agente.fig = plt.figure()
    agente.fig.suptitle('Trayectoria Exploración')
    
    # *-*-*-*-*-*-*-*-*-*-*-*-* Crear una subfigura *-*-*-*-*-*-*-*-*-*-*-*-*   
    # (Trayectoria experimental, obtenida de las revoluciones de las ruedas)
    agente.ax1 = agente.fig.add_subplot(111)

    # Configurar límites de los ejes
    agente.ax1.set_xlim(0, agente.size_x*10)
    agente.ax1.set_ylim(0, agente.size_y*10)

    # Configurar aspecto de los ejes
    agente.ax1.set_aspect('equal')
    agente.ax1.grid(True)
    
    
    plt.plot(agente.T_Exploracion_x, agente.T_Exploracion_y, '-o', color='red')
    plt.plot(agente.Pared_x_ds2,agente.Pared_y_ds2,'o', color='black')
    plt.plot(agente.Pared_x_ds4,agente.Pared_y_ds4,'o', color='black')
    plt.plot(agente.Pared_x_ds0,agente.Pared_y_ds0,'o', color='black')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Por posición de ruedas')
    plt.xlim(0,5)
    plt.ylim(0,5)
    plt.grid(True)

    plt.show()