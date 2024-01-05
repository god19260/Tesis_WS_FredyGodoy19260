import matplotlib.pyplot as plt
import keyboard


def graph_select(agente):
    print(" ")
    print("-------------------------------------------------------")
    print("d: mostrar datos\ns: mostrar stats")
    print("1: mostrar mapa\n2: mostrar obstaculos")
    print("3: mostrar procesamiento de espacio de trabjo\n4: mostrar Espacio de trabajo")
    print("5: mostrar Ruta óptima")
    print("n: salir")    

    select_process_flag = True
    while select_process_flag == True: 
        
        # cancelar el proceso de selección de gráfica
        if keyboard.is_pressed("n"):
            select_process_flag = False
        
        # selección de gráficas
        if keyboard.is_pressed("d"):
            while keyboard.is_pressed("d"):
                if agente.step(agente.timestep) == -1:
                    break
            Data(agente)

        if keyboard.is_pressed("s"):
            Error(agente)

        if keyboard.is_pressed("1"):
            Trayectoria_Exploracion(agente)
        
        if keyboard.is_pressed("2"):
            Obstaculos(agente)

        if keyboard.is_pressed("3"):
            Procesamiento_Espacio_Trabajo(agente)

        if keyboard.is_pressed("4"):
            Espacio_Trabajo(agente)

        if keyboard.is_pressed("5"):
            Ruta_Optima(agente)

        

        
        if agente.step(agente.timestep) == -1:
            break
            
        
        
def Data(agente):
    print("-------------------------------------------------------")
    print("------------------------ Datos ------------------------")
    print("Tiempo de simulación: ", int(agente.getTime()/60)," min")
    print("Pos x: ",round(agente.xc[-1]*100,0), "  -  ", round(agente.T_Exploracion_x[-1]*100,0), "  -  ", round(agente.T_Exploracion_GPS_x[-1]*100-agente.delta_GPS_Estimado_x*100))
    print("Pos wy: ",round(agente.yc[-1]*100,0), "  -  ", round(agente.T_Exploracion_y[-1]*100,0), "  -  ", round(agente.T_Exploracion_GPS_y[-1]*100-agente.delta_GPS_Estimado_y*100,0))
    print("Estimado: ", round(agente.phi,0), " - Real: ",agente.angulo)
        


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
    
    # Obtener los limites del mapa
    xlim=[0,0]
    ylim=[0,0]

    if min(agente.T_Exploracion_x) < xlim[0]: xlim[0] = min(agente.T_Exploracion_x)
    if max(agente.T_Exploracion_x) > xlim[1]: xlim[1] = max(agente.T_Exploracion_x)

    if min(agente.T_Exploracion_y) < ylim[0]: ylim[0] = min(agente.T_Exploracion_y)
    if max(agente.T_Exploracion_y) > ylim[1]: ylim[1] = max(agente.T_Exploracion_y)

    # Expandir el área de la gráfica
    xlim[0] = xlim[0]-1
    xlim[1] = xlim[1]+1

    ylim[0] = ylim[0]-1
    ylim[1] = ylim[1]+1

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Por posición de ruedas')
    plt.xlim(xlim)
    plt.ylim(ylim)
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
    
    # Obtener los limites del mapa
    xlim=[0,0]
    ylim=[0,0]

    if min(agente.T_Exploracion_GPS_x) < xlim[0]: xlim[0] = min(agente.T_Exploracion_GPS_x)
    if max(agente.T_Exploracion_GPS_x) > xlim[1]: xlim[1] = max(agente.T_Exploracion_GPS_x)

    if min(agente.T_Exploracion_GPS_y) < ylim[0]: ylim[0] = min(agente.T_Exploracion_GPS_y)
    if max(agente.T_Exploracion_GPS_y) > ylim[1]: ylim[1] = max(agente.T_Exploracion_GPS_y)

    # Expandir el área de la gráfica
    xlim[0] = xlim[0]-1
    xlim[1] = xlim[1]+1

    ylim[0] = ylim[0]-1
    ylim[1] = ylim[1]+1

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('GPS')
    plt.xlim(xlim)
    plt.ylim(ylim)
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
    
    agente.ax1 = agente.fig.add_subplot(111)

    # Configurar límites de los ejes
    agente.ax1.set_xlim(0, agente.size_x*10)
    agente.ax1.set_ylim(0, agente.size_y*10)

    # Configurar aspecto de los ejes
    agente.ax1.set_aspect('equal')
    agente.ax1.grid(True)
    
    
    plt.plot(agente.T_Exploracion_x, agente.T_Exploracion_y, '-o', color='red')
    
    plt.plot(agente.Pared_x_ds0,agente.Pared_y_ds0,'o', color='black')
    plt.plot(agente.Pared_x_ds1,agente.Pared_y_ds1,'o', color='black')
    plt.plot(agente.Pared_x_ds2,agente.Pared_y_ds2,'o', color='black')
    #plt.plot(agente.Pared_x_ds3,agente.Pared_y_ds3,'o', color='black')
    plt.plot(agente.Pared_x_ds4,agente.Pared_y_ds4,'o', color='black')
    plt.plot(agente.Pared_x_ds5,agente.Pared_y_ds5,'o', color='black')

    # Obtener los limites del mapa
    xlim=[0,0]
    ylim=[0,0]

    if min(agente.T_Exploracion_x) < xlim[0]: xlim[0] = min(agente.T_Exploracion_x)
    if max(agente.T_Exploracion_x) > xlim[1]: xlim[1] = max(agente.T_Exploracion_x)

    if min(agente.T_Exploracion_y) < ylim[0]: ylim[0] = min(agente.T_Exploracion_y)
    if max(agente.T_Exploracion_y) > ylim[1]: ylim[1] = max(agente.T_Exploracion_y)

    # Expandir el área de la gráfica
    xlim[0] = xlim[0]-1
    xlim[1] = xlim[1]+1

    ylim[0] = ylim[0]-1
    ylim[1] = ylim[1]+1


    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Por posición de ruedas')
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.grid(True)

    plt.show()

def Procesamiento_Espacio_Trabajo(agente):
    # ------------------------- Crear una figura -------------------------- 
    # */*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
    # */*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
    agente.fig3 = plt.figure()
    agente.fig3.suptitle('Espacio de trabajo')
    # */*/*/*/*/*/*/*/*/*/*/*/* Crear una subfigura */*/*/*/*/*/*/*/*/*/*/*
    agente.ax1_fig3 = agente.fig3.add_subplot(121)

    # Configurar límites de los ejes
    agente.ax1_fig3.set_xlim(-5,50)
    agente.ax1_fig3.set_ylim(-5,50)

    # Configurar aspecto de los ejes
    agente.ax1_fig3.set_aspect('equal')
    agente.ax1_fig3.grid(True)
    
    plt.title('mapa 2D')
    plt.plot(agente.WS_x,agente.WS_y,'.',color='blue')
    #plt.plot((agente.factorWS*agente.x_vehiculo),(agente.factorWS*agente.y_vehiculo),'o',color = 'red')
    plt.xlabel('x')
    plt.ylabel('y')     
    # */*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
    # *-*-*-*-*-*-*-*-*-*-*-*-* Crear una subfigura *-*-*-*-*-*-*-*-*-*-*-*-*   
    # (Trayectoria experimental, obtenida de las revoluciones de las ruedas)
    agente.ax2_fig3 = agente.fig3.add_subplot(122)

    # Configurar límites de los ejes
    agente.ax2_fig3.set_xlim(0, agente.size_x*10)
    agente.ax2_fig3.set_ylim(0, agente.size_y*10)

    # Configurar aspecto de los ejes
    agente.ax2_fig3.set_aspect('equal')
    agente.ax2_fig3.grid(True)
    
    
    
    
    
    plt.plot(agente.Pared_x_ds0,agente.Pared_y_ds0,'o', color='black')
    plt.plot(agente.Pared_x_ds1,agente.Pared_y_ds1,'o', color='black')
    plt.plot(agente.Pared_x_ds2,agente.Pared_y_ds2,'o', color='black')
    plt.plot(agente.Pared_x_ds3,agente.Pared_y_ds3,'o', color='black')
    plt.plot(agente.Pared_x_ds4,agente.Pared_y_ds4,'o', color='black')
    plt.plot(agente.Pared_x_ds5,agente.Pared_y_ds5,'o', color='black')
    
    plt.plot((agente.x_vehiculo),(agente.y_vehiculo),'o',color = 'red')
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Por posición de ruedas')
    plt.xlim(0,5)
    plt.ylim(0,5)
    plt.grid(True)

    plt.show()

def Espacio_Trabajo(agente):    
    mapa = agente.mapa_WS
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
    #plt.plot(int(agente.factorWS*(agente.x_vehiculo)),int(agente.factorWS*(agente.y_vehiculo)),'o',color = 'red')
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

    plt.plot(int(agente.factorWS*(agente.x_vehiculo)),int(agente.factorWS*(agente.y_vehiculo)),'o',color = 'red')
    # Mostrar la gráfica
    plt.show()

def Ruta_Optima(agente):
    mapa = agente.mapa_WS
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
        agente.x_rutaOptima = [posicion[1]+0.5 for posicion in agente.ruta_optima]
        agente.y_rutaOptima = [posicion[0]+0.5 for posicion in agente.ruta_optima]
        #plt.plot(inicio[1]+0.5,inicio[0]+0.5,'-o',color='blue')
        
        plt.plot(agente.x_rutaOptima, agente.y_rutaOptima, '-o', color='green')
        plt.plot(agente.x_rutaOptima[0], agente.y_rutaOptima[0], '-o', color='blue')
        plt.plot(agente.objetivo_x, agente.objetivo_y, '-o', color='red')
        

        #plt.plot(agente.x_rutaOptima[0],agente.y_rutaOptima[0],'o',color = 'red')
        #plt.plot(int(agente.factorWS*(agente.x_vehiculo))+abs(agente.min_val_x),int(agente.factorWS*(agente.y_vehiculo))+abs(agente.min_val_y),'o',color = 'blue')
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
        plt.plot( agente.x_rutaOptima,  agente.y_rutaOptima, 'o', color='green')
        plt.plot( agente.x_rutaOptima[0], agente.y_rutaOptima[0],'o',color = 'red')
        
    except:
        print("No se generó ruta óptima, verificar puntos seleccionados.")    
    
    
    # Mostrar la gráfica
    plt.show()
