import numpy as np
import matplotlib.pyplot as plt

# Se define un mapa aleatorio
filas = 20
columnas = 20
mapa = np.zeros((filas, columnas))

# Generar obstáculos al azar
for i in range(130):  # Número de obstáculos que deseas generar
    fila = np.random.randint(0, filas)  # Fila aleatoria
    columna = np.random.randint(0, columnas)  # Columna aleatoria
    mapa[fila, columna] = 1  # Establecer el elemento como un obstáculo (1)

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
