import matplotlib.pyplot as plt
import numpy as np

Angulos=  [45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,135,130,125,120,115,110,105,100,95,90,85,80,75,70,65,60,55,50,45]
#Distancias= [318,321,324,325,325,331,323,333,330,325,324,319,318,320,318,322,318,318,313,312,309,314,321,316,316,321,317,327,324,326,328,328,326,328,323,325,322,326,327]
Distancias = [169,169,166,166,168,166,164,165,167,165,165,164,165,166,166,163,167,167,164,166,164,166,165,166,167,164,164,166,166,165,165,167,167,167,169,165,167,168,170]




print(len(Distancias), '  --  ',len(Angulos))


# ------------------------------ Análisis de datos ------------------------------ 

# Calcular la varianza
variance = np.var(Distancias)
promedio = np.average(Distancias)
print("Variaza: ",variance, " mm")
print("Promedio: ",promedio, " mm")

# ------------------------------ Gráfica ------------------------------ 
plt.plot(Angulos, Distancias, 'o',color='black')


plt.xlabel('grados')
plt.ylabel('Distancia mm')
plt.title('Prueba sensor VL53L0, rotación de 45° a 140°')

plt.savefig('16cm.png')
plt.show()


