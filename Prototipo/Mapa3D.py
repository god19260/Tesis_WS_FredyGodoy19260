import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

mapa = np.array([[0,0,0,0,0,0,0,1,0,0,0],
                 [1,0,0,0,1,0,0,0,0,1,1],
                 [1,0,0,0,0,1,0,0,1,1,0],
                 [0,0,1,0,0,0,0,0,0,1,0],
                 [0,0,1,1,1,0,0,0,0,0,0],
                 [0,0,1,1,0,0,0,0,0,0,0],
                 [0,0,0,0,0,1,0,1,0,1,0]])

# Obtener las dimensiones del mapa
mapa_flip = np.flip(mapa,axis=0)
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
        if mapa_flip[fila, columna] == 1:
            # Dibujar obstáculo
            rect = plt.Rectangle((columna, fila), 1, 1, facecolor='black')
            ax1.add_patch(rect)

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
        if mapa_flip[fila, columna] == 1:
            # Dibujar obstáculo como una caja
            x = columna
            y = fila
            z = 0
            dx = 1
            dy = 1
            dz = 1
            ax2.bar3d(x, y, z, dx, dy, dz, color='black')

# Mostrar la gráfica
plt.show()
