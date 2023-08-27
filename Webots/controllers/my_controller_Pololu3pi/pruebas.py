import numpy as np

x = [1,2,3]
y = [3,4,5]



# Calcular las dimensiones de la matriz basadas en los valores máximos de x e y
num_filas = max(y) +1
num_columnas = max(x)+1

# Crear una matriz llena de ceros
matriz = np.zeros((num_filas, num_columnas))

# Asignar el valor 1 en las coordenadas proporcionadas por x e y
for i in range(len(x)):
    matriz[y[i]][x[i]] = 1

print(matriz)