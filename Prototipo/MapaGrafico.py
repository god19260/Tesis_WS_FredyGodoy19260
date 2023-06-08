"""

mapa = [[1,0,0,0,0,0,0,1,0,1,0],
        [1,0,0,0,1,0,0,1,0,1,0],
        [1,0,0,0,0,1,0,1,0,1,0],
        [1,0,1,0,0,0,0,1,0,1,0],
        [1,0,0,0,1,0,0,1,0,1,0],
        [1,0,1,0,0,1,0,1,0,1,0],
        [1,0,0,0,0,1,0,1,0,1,0]]
"""

import numpy as np
import matplotlib.pyplot as plt

# Definir el mapa
# Mapa: cada espacio representa un cuadrado de 0.25m 

mapa = np.array([[1,0,0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,1,0,1],
                 [1,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0],
                 [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,1],
                 [0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1],
                 [0,0,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0],
                 [0,0,1,1,0,0,0,0,0,0,0,1,0,0,1,0,1,1,0,0],
                 [0,0,0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,1,0,0],
                 [1,0,0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,1,0,1],
                 [1,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0],
                 [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,1],
                 [0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1],
                 [0,0,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0],
                 [1,0,0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,1,0,1],
                 [1,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0],
                 [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,1],
                 [0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1],
                 [0,0,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0],
                 [1,0,0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,1,0,1],
                 [1,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0],
                 [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,1]])

# Obtener las dimensiones del mapa
mapa_flip = np.flip(mapa,axis=0)
filas, columnas = mapa.shape

# Crear una figura y ejes
fig, ax = plt.subplots()

# Configurar límites de los ejes
ax.set_xlim(0, columnas)
ax.set_ylim(0, filas)

# Configurar aspecto de los ejes
ax.set_aspect('equal')
ax.grid(True)

# Iterar sobre el mapa y graficar obstáculos
for fila in range(filas):
    for columna in range(columnas):
        if mapa_flip[fila, columna] == 1:
            # Dibujar obstáculo
            rect = plt.Rectangle((columna, fila), 1, 1, facecolor='black')
            ax.add_patch(rect)

# Mostrar la solución gráficamente
plt.show()
