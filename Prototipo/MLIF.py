
# Fusión del mapa multi-agente (MLIF)
# Etapa 3 del método Multi-Stage Optimization (MSO)

import numpy as np
import matplotlib.pyplot as plt

def fusionar_mapas(mapa1, mapa2):
    # Verificar las dimensiones de los mapas
    if mapa1.shape != mapa2.shape:
        raise ValueError("Los mapas deben tener la misma dimensión")

    # Crear un mapa vacío para almacenar la fusión
    mapa_fusionado = np.zeros_like(mapa1)

    # Iterar sobre cada celda de los mapas
    for i in range(mapa1.shape[0]):
        for j in range(mapa1.shape[1]):
            # Obtener los valores de cada celda en los mapas
            valor_mapa1 = mapa1[i, j]
            valor_mapa2 = mapa2[i, j]

            # Realizar la fusión de acuerdo al algoritmo MLIF
            if valor_mapa1 == 1 or valor_mapa2 == 1:
                mapa_fusionado[i, j] = 1

    return mapa_fusionado

# Definir los mapas de ejemplo
mapa1 = np.array([[1,0,0,0,0,0,0,1,0,0,0],
                  [1,0,0,0,1,0,0,0,0,1,1],
                  [1,0,0,0,0,1,0,0,1,1,0],
                  [0,0,1,0,0,0,0,0,0,1,0],
                  [0,0,1,1,1,0,0,0,0,0,0],
                  [0,0,1,1,0,0,0,0,0,0,0],
                  [0,0,0,0,0,1,0,1,0,1,0]])

mapa2 = np.array([[0,1,0,0,0,0,1,0,0,0,0],
                  [0,0,1,0,1,0,0,0,0,1,1],
                  [1,0,0,0,0,1,0,0,1,1,0],
                  [0,0,0,1,0,0,0,0,0,1,0],
                  [0,0,1,1,1,0,0,0,0,0,0],
                  [0,0,1,1,0,0,0,0,0,0,0],
                  [0,0,0,0,0,1,0,1,0,1,0]])


# Fusionar los mapas
mapa_fusionado = fusionar_mapas(mapa1, mapa2)


# Obtener las dimensiones del mapa
mapa_flip = np.flip(mapa_fusionado,axis=0)
filas, columnas = mapa_fusionado.shape

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