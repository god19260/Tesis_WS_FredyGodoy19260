import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Cargar la imagen
image_path = "D:\UVG_1Ciclo_2023\Tesis\Tesis_WS_FredyGodoy19260\Fotos\pololuOnShape_Isometrica_BaseSensores_1.png"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Obtener las dimensiones de la imagen
height, width = image.shape

# Crear una cuadrícula 3D basada en las dimensiones de la imagen
x = np.arange(0, width, 1)
y = np.arange(0, height, 1)
x, y = np.meshgrid(x, y)

# Convertir la imagen en una matriz de puntos 3D
z = image / 255.0  # Normalizar los valores para obtener alturas entre 0 y 1

# Crear una figura 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Graficar la superficie 3D
ax.plot_surface(x, y, z, cmap='viridis')

# Configurar etiquetas de los ejes
ax.set_xlabel('Ancho (píxeles)')
ax.set_ylabel('Altura (píxeles)')
ax.set_zlabel('Intensidad (normalizada)')

# Mostrar el gráfico en 3D
plt.show()