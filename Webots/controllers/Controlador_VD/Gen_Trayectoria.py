import numpy as np
import matplotlib.pyplot as plt
import heapq

def dijkstra(mapa,ox,oy,dx,dy):
    filas, columnas = mapa.shape
    # Definir punto de inicio y final
    inicio = [ox,oy]
    while mapa[inicio[1],inicio[0]] == 1:
        inicio[0] = inicio[0]+1
        inicio[1] = inicio[1]+1
    final = [dx,dy]


    inicio = (inicio[1],inicio[0])
    final = (final[1],final[0])

    # Definir los movimientos permitidos (arriba, abajo, izquierda, derecha) y (diagonales)
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]    
                #,(1,1), (-1,1), (-1,-1), (1,-1)]

    # Función para obtener los vecinos válidos de una posición en el mapa
    def obtener_vecinos(posicion):
        fila, columna = posicion
        vecinos = []

        for movimiento in movimientos:
            nueva_fila = fila + movimiento[0]
            nueva_columna = columna + movimiento[1]

            if nueva_fila >= 0 and nueva_fila < filas and nueva_columna >= 0 and nueva_columna < columnas and mapa[nueva_fila, nueva_columna] == 0:
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
    return ruta_optima