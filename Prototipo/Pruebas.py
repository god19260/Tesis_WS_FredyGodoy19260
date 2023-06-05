import random
import sys
import math
import matplotlib.pyplot as plt

# Elige un paso para una hormiga, teniendo en cuenta los valores
# las feromonas y descartando los nodos ya visitados.
def eligeNodo(valors, ferom, visitados):
    #Se calcula la tabla de pesos de cada ciudad
    listaValores  = []
    disponibles = []
    actual      = visitados[-1]

    # Influencia de cada valor (alfa: feromonas; beta: valor)
    alfa = 1.0
    beta = 0.5

    # El parámetro beta (peso de los valores) es 0.5 y alfa=1.0
    for i in range(len(valors)):
        if i not in visitados:
            fer  = math.pow((1.0 + ferom[actual][i]), alfa)
            peso = math.pow(1.0/valors[actual][i], beta) * fer
            disponibles.append(i)
            listaValores.append(peso)

    # Se elige aleatoriamente una de los nodos disponibles,
    # teniendo en cuenta su peso relativo.
    valor     = random.random() * sum(listaValores)
    acumulado = 0.0
    i         = -1
    while valor > acumulado:
        i         += 1
        acumulado += listaValores[i]

    return disponibles[i]

# Genera una "hormiga", que eligirá un camino (nodos que visita) teniendo en cuenta
# los valores y los rastros de feromonas. Devuelve una tupla
# con el camino (nodos visitados) y su longCamino (Suma de valores).
def eligeCamino(matriz, feromonas):
    # El nodo inicial siempre es el 0
    camino     = [0]
    longCamino = 0

    # Elegir cada paso según los valores y las feromonas
    while len(camino) < len(matriz):
        nodo      = eligeNodo(matriz, feromonas, camino)
        longCamino += matriz[camino[-1]][nodo]
        camino.append(nodo)

    # Para terminar hay que volver al nodo de origen (0)
    longCamino += matriz[camino[-1]][0]
    camino.append(0)

    return (camino, longCamino)

# Actualiza la matriz de feromonas siguiendo el camino recibido
def rastroFeromonas(feromonas, camino, dosis):
    for i in range(len(camino) - 1):
        feromonas[camino[i]][camino[i+1]] += dosis

# Evapora todas las feromonas multiplicándolas por una constante
# = 0.9 (en otras palabras, el coeficiente de evaporación es 0.1)
def evaporaFeromonas(feromonas):
    for lista in feromonas:
        for i in range(len(lista)):
            lista[i] *= 0.9

# Resuelve el problema del viajante de comercio mediante el
# algoritmo de la colonia de hormigas. Recibe una matriz de
# distancias y devuelve una tupla con el mejor camino que ha
# obtenido (lista de índices) y su longitud.
def hormigas(matriz, iteraciones, distMedia):
    # Primero se crea una matriz de feromonas vacía
    n = len(matriz)
    feromonas = [[0 for i in range(n)] for j in range(n)]

    # El mejor camino y su longitud (inicialmente "infinita")
    mejorCamino     = []
    longMejorCamino = sys.maxsize

    # En cada iteración se genera una hormiga, que elige un camino,
    # y si es mejor que el mejor que teníamos, deja su rastro de
    # feromonas (mayor cuanto más corto sea el camino)
    for iter in range(iteraciones):
        (camino, longCamino) = eligeCamino(matriz, feromonas)

        if longCamino <= longMejorCamino:
            mejorCamino     = camino
            longMejorCamino = longCamino

        rastroFeromonas(feromonas, camino, distMedia/longCamino)
        # En cualquier caso, las feromonas se van evaporando
        evaporaFeromonas(feromonas)

    # Se devuelve el mejor camino que se haya encontrado
    return (mejorCamino, longMejorCamino)


# Hemos encontrado un método que nos genera una matriz con nodos xdistantes

# Genera una matriz de valores de n x n, asignando valores aleatorios y poniendo un valor tope
# Los valores de un nodo A a un nodo B son los mismos que de un nodo B a A, siendo A y B dos nodos cualesquiera
# Le asignamos valores aleatorios
def matrizDistancias(n, distanciaMaxima):
    matriz = [[0 for i in range(n)] for j in range(n)]

    for i in range(n):
        for j in range(i):
            matriz[i][j] = i + 1
            matriz[j][i] = matriz[i][j]

    return matriz


# Ejemplo de uso
# Generación de una matriz de prueba
numCiudades      = 2
distanciaMaxima  = 1
ciudades         = matrizDistancias(numCiudades, distanciaMaxima)
print(ciudades)

# Obtención del mejor camino, las iteraciones son la cantidad de hormigas que empleamos para resolverlo
iteraciones = 1000
distMedia   = numCiudades * distanciaMaxima / 2
(camino, longCamino) = hormigas(ciudades, iteraciones, distMedia)
print("Camino: ", camino)
print("Longitud del camino: ", longCamino)

# Graficar el camino
x = [ciudades[i][0] for i in camino]
y = [ciudades[i][1] for i in camino]

plt.plot(x, y, 'ro-')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Camino óptimo')
plt.grid(True)
plt.show()
