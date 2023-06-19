import numpy as np
import matplotlib.pyplot as plt
import heapq

# Mapa a usar
# 1: Mapa aleatorio
# 2 en adelante: Mapas guardados
tipoMapa = 2

if tipoMapa ==1:
    # Se define un mapa aleatorio
    filas = 20
    columnas = 20
    mapa = np.zeros((filas, columnas))
    
    # Generar obstáculos al azar
    for i in range(150):  # Número de obstáculos que deseas generar
        fila = np.random.randint(0, filas)  # Fila aleatoria
        columna = np.random.randint(0, columnas)  # Columna aleatoria
        mapa[fila, columna] = 1  # Establecer el elemento como un obstáculo (1)
    print(mapa)

elif tipoMapa == 2:
    # Mapa definido 1
    mapa = np.array([[1,0,0,0,0,0,0,1,0,0,0],
                    [1,0,0,0,1,0,0,0,0,1,1],
                    [1,0,0,0,0,1,0,0,1,1,0],
                    [0,0,1,0,0,0,0,0,0,1,0],
                    [0,0,1,1,1,0,0,0,0,0,0],
                    [0,0,1,1,0,0,0,0,0,0,0],
                    [0,0,0,0,0,1,0,1,0,1,0]])
    # Obtener las dimensiones del mapa
    filas, columnas = mapa.shape

    
elif tipoMapa ==3:
    # Mapa definido 2
    mapa = np.array([[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
                    [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0,],
                    [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1,],
                    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0,],
                    [0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0,],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0,],
                    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0,],
                    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
                    [0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,],
                    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,],
                    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0,],
                    [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1,],
                    [0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
                    [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0,],
                    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0,],
                    [1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0,],
                    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0,],
                    [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0,],
                    [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0,]])
    # Obtener las dimensiones del mapa
    filas, columnas = mapa.shape


mapa_flip = np.flip(mapa,axis=0)

# Definir punto de inicio y final
inicio = [columnas-1,0]
while mapa_flip[inicio[1],inicio[0]] == 1:
    inicio[0] = inicio[0]+1
    inicio[1] = inicio[1]+1
final = [0, filas-1]


inicio = (inicio[1],inicio[0])
final = (final[1],final[0])

# Definir los movimientos permitidos (arriba, abajo, izquierda, derecha) y (diagonales)
movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)
               ,(1,1), (-1,1), (-1,-1), (1,-1)]

# Función para obtener los vecinos válidos de una posición en el mapa
def obtener_vecinos(posicion):
    fila, columna = posicion
    vecinos = []

    for movimiento in movimientos:
        nueva_fila = fila + movimiento[0]
        nueva_columna = columna + movimiento[1]

        if nueva_fila >= 0 and nueva_fila < filas and nueva_columna >= 0 and nueva_columna < columnas and mapa_flip[nueva_fila, nueva_columna] == 0:
            vecinos.append((nueva_fila, nueva_columna))

    return vecinos

# Función para calcular la distancia entre dos posiciones
def calcular_distancia(posicion1, posicion2):
    fila1, columna1 = posicion1
    fila2, columna2 = posicion2
    return np.sqrt((fila2 - fila1) ** 2 + (columna2 - columna1) ** 2)

# Función para encontrar la ruta más corta utilizando el algoritmo de Dijkstra
def encontrar_ruta_optima(inicio, final):
    distancia = np.full((filas, columnas), np.inf)
    visitado = np.zeros((filas, columnas), dtype=bool)
    distancia[inicio] = 0
    heap = [(0, inicio, [])]

    while heap:
        _, posicion_actual, ruta_actual = heapq.heappop(heap)

        flag = True
        if posicion_actual == final:
            return ruta_actual,flag

        for vecino in obtener_vecinos(posicion_actual):
            nueva_distancia = distancia[posicion_actual] + calcular_distancia(posicion_actual, vecino)

            if nueva_distancia < distancia[vecino]:
                distancia[vecino] = nueva_distancia
                heapq.heappush(heap, (nueva_distancia, vecino, ruta_actual + [vecino]))
    flag = False
    return (ruta_actual,flag)

# Encontrar la ruta óptima
(ruta_optima,flag) = encontrar_ruta_optima(inicio, final)
#print(ruta_optima)

# Graficar el mapa con la ruta óptima
fig, ax = plt.subplots()
ax.set_xlim(0, columnas)
ax.set_ylim(0, filas)
ax.set_aspect('equal')
ax.grid(True)

# Graficar obstáculos
for fila in range(filas):
    for columna in range(columnas):
        if mapa_flip[fila, columna] == 1:
            rect = plt.Rectangle((columna, fila), 1, 1, facecolor='black')
            ax.add_patch(rect)

# Graficar ruta óptima
try:
    x = [posicion[1] + 0.5 for posicion in ruta_optima]
    y = [posicion[0] + 0.5 for posicion in ruta_optima]
    plt.plot(inicio[1]+0.5,inicio[0]+0.5,'-o',color='blue')
    if flag == True:
        plt.plot(x, y, '-o', color='green')
    else:
        plt.plot(x, y, '-o', color='red')
except:
    print("Error al graficar ruta")
# Mostrar la solución gráficamente
plt.show()