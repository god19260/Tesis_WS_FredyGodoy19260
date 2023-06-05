from telnetlib import NOP
import tkinter as tk
from tkinter import *
from turtle import right
from tkinter.messagebox import showinfo
from tkinter import Tk, filedialog as fd
import math
from sympy import *
import sympy as sym
import numpy as np



class Proyecto(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.GridNormal = tk.PhotoImage(file="./Imagen_Proyecto1/Grid_Normal2.png")
        #self.GridLog = tk.PhotoImage(file='./Imagen_Proyecto1/Grid_Log.png')
        # variables a usar
        self.previous_x = self.previous_y = 0
        self.x = self.y = 0
        self.Puntos = []
        self.puntos_confirmar = []
        self.sizex = 800
        self.sizey = 600
        self.cor_x,self.cor_y = [],[]
        self.color_linea = "black"

        # definir el espacio para trazar lineas
        self.canvas = tk.Canvas(self, width=self.sizex ,height=self.sizey, bg = "white", cursor="cross")
        #self.canvas.create_image(400,250,image=self.GridNormal, anchor="center")    # Por default fondo normal
        self.canvas.pack(side="top", fill="both", expand=True)

        menu = tk.Menu(self)
        self.config(menu = menu)
        Fondo  = tk.Menu(menu)
        Fondo.add_command(label = "Grid normal",command=self.BG_GridNormal)
        Fondo.add_command(label = "Imagen",command = self.select_file)
        Fondo.add_command(label = "Negro",command = self.BG_Negro)
        Fondo.add_command(label = "Blanco",command = self.BG_Blanco)
        menu.add_cascade(label = "Fondo",menu = Fondo)

        Linea = tk.Menu(menu)
        Linea.add_command(label = "Negro",command=self.L_Negra)
        Linea.add_command(label = "Blanco",command=self.L_Blanca)
        Linea.add_command(label = "Rojo",command=self.L_Roja)
        Linea.add_command(label = "Amarillo",command=self.L_Amarilla)
        menu.add_cascade(label = "Color Linea",menu = Linea)

        Metodo = tk.Menu(menu)
        Metodo.add_command(label = "Lineal",command=self.Lineal)
        Metodo.add_command(label = "Exponencial",command=self.Exponencial)
        Metodo.add_command(label = "Potencias",command=self.Potencias)
        Metodo.add_command(label = "Saturación",command=self.Saturacion)
        Metodo.add_command(label = "Inter. Lagrange",command=self.Inter_Lagrange)
        menu.add_cascade(label = "Metodo",menu = Metodo)
         
        # botones
        #self.button_Calcular = tk.Button(self, text = "Determinar función", command = self.print_points)
        #self.button_Calcular.pack(side="top", fill="both")

        self.button_clear = tk.Button(self, text = "Limpiar", command = self.clear_all)
        self.button_clear.pack(side="top", fill="both")

        self.canvas.bind("<Motion>", self.tell_me_where_you_are)
        self.canvas.bind("<B1-Motion>", self.draw_from_where_you_are)
        # B1-Motion, click izquierdo
        # B2-Motion, click rueda
        # B3-Motion, click derecho 
        self.info = ""
        self.T = tk.Text(self, height = 6, width = 100)
        self.T.pack(side = "top")
        self.T.insert(tk.END,self.info)
        
    def clear_all(self):
        self.canvas.delete("linea")
        self.canvas.delete("puntos")
        self.Puntos[:] = []
        self.cor_x[:],self.cor_y[:] = [],[]
        self.puntos_confirmar[:] = []

    def print_points(self):
        try:
            if self.Puntos:
                self.Puntos.pop()
                self.Puntos.pop()
            self.canvas.create_line(self.puntos_confirmar, fill = "red",tag = "linea")
            
            #self.points_recorded[:] = []
        except:
            print("No hay cambios en los puntos")
        

    def tell_me_where_you_are(self, event):
        self.previous_x = event.x
        self.previous_y = event.y

    def draw_from_where_you_are(self, event):
        #if self.points_recorded:
        #    self.points_recorded.pop()
        #    self.points_recorded.pop()

        self.x = event.x
        self.y = event.y
        self.canvas.create_line(self.previous_x, self.previous_y, 
                                self.x, self.y,fill=self.color_linea,tag = "puntos")
        #self.points_recorded.append(self.previous_x-self.sizex/2)
        #self.points_recorded.append(self.sizey/2-self.previous_y)
        
        self.Puntos.append(self.x-self.sizex/2)     
        self.Puntos.append(self.sizey/2-self.y)

        self.puntos_confirmar.append((self.x-self.sizex/2)+self.sizex/2)
        self.puntos_confirmar.append(-(self.sizey/2-self.y)+self.sizey/2)


        self.previous_x = self.x
        self.previous_y = self.y
    
    def BG_GridNormal(self):
        self.canvas.delete("imagen")
        self.canvas.create_image(self.sizex/2,self.sizey/2,image=self.GridNormal, anchor="center",tag= "gridnormal")    # Por default fondo normal
    def BG_Negro(self):
        self.canvas.delete("imagen")
        self.canvas.delete("gridnormal")
        self.canvas.configure(bg = "black")
    def BG_Blanco(self):
        self.canvas.delete("imagen")
        self.canvas.delete("gridnormal")
        self.canvas.configure(bg = "white")
    def L_Negra(self):
        self.color_linea = "black"
        self.T.delete("1.0",tk.END)
        self.T.insert(END,"Se cambio el color de linea a negro")
        
    def L_Roja(self):
        self.color_linea = "red"
        self.T.delete("1.0",tk.END)
        self.T.insert(END,"Se cambio el color de linea a rojo")
    def L_Blanca(self):
        self.color_linea = "white"
        self.T.delete("1.0",tk.END)
        self.T.insert(END,"Se cambio el color de linea a blanco")
    def L_Amarilla(self):
        self.color_linea = "yellow"    
        self.T.delete("1.0",tk.END)
        self.T.insert(END,"Se cambio el color de linea a amarillo")

    def select_file(self):
        
        filetypes = (
            ('text files', '*.jpg'),
            ('text files', '*.png'),
            ('All files', '*.*')
        )

        nombre_archivo = fd.askopenfilename(
            title='Open a file',
            #initialdir='/',
            filetypes=filetypes)

        # colocar la imagen seleccionada como fondo 
        self.canvas.delete("gridnormal")
        self.fondo_imagen = tk.PhotoImage(file=nombre_archivo)
        self.canvas.create_image(self.sizex/2,self.sizey/2,image=self.fondo_imagen, anchor="center",tag = "imagen")
                
    def Lineal(self):
        self.cor_x[:],self.cor_y[:] = [],[]
        try:
            contador_i = 0 
            x_y = "x"
            while contador_i < len(self.Puntos):
                if x_y == "x":
                    self.cor_x.append(float(self.Puntos[contador_i]))
                    x_y = "y"
                else:
                    self.cor_y.append(float(self.Puntos[contador_i]))
                    x_y = "x"
                contador_i = contador_i + 1
            #print(f"\n\n{self.Puntos}\n{self.cor_x}\n{self.cor_y}")
            
            n = len(self.cor_x)
            x2,y2 = 0,0
            r2 = 0
            
            # ------------ Proceso de calculo ----------------------
            contador_i = 0
            x_sum,y_sum = 0,0
            x2_sum,y2_sum,xy_sum,YmYp_2_sum = 0,0,0,0
            yma0ma1x_2_sum = 0
            while contador_i <= (len(self.cor_x)-1):
                x_sum = x_sum + self.cor_x[contador_i]
                y_sum = y_sum + self.cor_y[contador_i]
                contador_i = contador_i+1

            yp = y_sum/n

            contador_i = 0
            while contador_i <= (len(self.cor_x)-1):
                x2 = (self.cor_x[contador_i])**2
                y2 = (self.cor_y[contador_i])**2
                xy = self.cor_x[contador_i]*self.cor_y[contador_i]
                YmYp_2 = (self.cor_y[contador_i]-yp)**2       # (y - yp)^2   

                x2_sum = x2_sum + x2
                y2_sum = y2_sum + y2
                xy_sum = xy_sum + xy
                YmYp_2_sum = YmYp_2_sum + YmYp_2

                contador_i = contador_i + 1
            
            a0 = (x2_sum*y_sum-x_sum*xy_sum)/(n*x2_sum-x_sum**2)
            a1 = (n*xy_sum-x_sum*y_sum)/(n*x2_sum-x_sum**2)
            contador_i = 0 
            while contador_i <= (len(self.cor_x)-1):
                yma0ma1x_2 = (self.cor_y[contador_i]-a0-a1*self.cor_x[contador_i])**2
                yma0ma1x_2_sum = yma0ma1x_2_sum + yma0ma1x_2
                contador_i = contador_i + 1 

            r2 = (YmYp_2_sum-yma0ma1x_2_sum)/YmYp_2_sum
            
            # print(f'x sum: {x_sum}')
            # print(f'y sum: {y_sum}')
            # print(f'x2 sum: {x2_sum}')
            # print(f'xy sum: {xy_sum}')
            # print(f'(y-yp)^2: {YmYp_2_sum}')
            # print(f'(y-a0-a1x)^2: {yma0ma1x_2_sum}')
            # print(f'yp: {yp}')
            # print(f'n: {n}')
            print("\nMetodo Lineal")
            print(f'r^2: {r2}')
            print(f'a0:  {a0}')
            print(f'a1:  {a1}')
            print(f"Funcion: y = {a1}x+({a0})")
            self.T.delete("1.0",tk.END)
            self.T.insert(END,"*-*-*-*-* Metodo Lineal *-*-*-*-*\n")
            self.T.insert(END,f" a0  = {a0}\n a1  = {a1}\n r^2 = {r2}\n")
            self.T.insert(END,f" y = {a1}x+{a0}\n")    
                
        except:
            print("Ingresar puntos nuevos")
        
    def Exponencial(self):
        self.cor_x[:],self.cor_y[:] = [],[]
        try:
            contador_i = 0 
            x_y = "x"
            while contador_i < len(self.Puntos):
                if x_y == "x":
                    self.cor_x.append(float(self.Puntos[contador_i]))
                    x_y = "y"
                else:
                    self.cor_y.append(float(self.Puntos[contador_i]))
                    x_y = "x"
                contador_i = contador_i + 1
            #print(f"\n\n{self.Puntos}\n{self.cor_x}\n{self.cor_y}")
            n = len(self.cor_x)
            x2,y2 = 0,0
            r2 = 0
            yt = []
            contador_i = 0
            while contador_i < len(self.cor_x):
                yt_temp = np.log(self.cor_y[contador_i])
                yt.append(yt_temp)
                contador_i = contador_i + 1

            # ------------ Proceso de calculo ----------------------
            x_sum,yt_sum = 0,0
            x2_sum,y2_sum,xy_sum,YmYp_2_sum = 0,0,0,0
            yma0ma1x_2_sum = 0
            contador_i = 0
            while contador_i <= (len(self.cor_x)-1):
                x_sum = x_sum + self.cor_x[contador_i]
                yt_sum = yt_sum + yt[contador_i]
                contador_i = contador_i+1

            yp = yt_sum/n

            contador_i = 0
            while contador_i <= (len(self.cor_x)-1):
                x2 = (self.cor_x[contador_i])**2
                y2 = (yt[contador_i])**2
                xy = self.cor_x[contador_i]*yt[contador_i]
                YmYp_2 = (yt[contador_i]-yp)**2       # (y - yp)^2   

                x2_sum = x2_sum + x2
                y2_sum = y2_sum + y2
                xy_sum = xy_sum + xy
                YmYp_2_sum = YmYp_2_sum + YmYp_2

                contador_i = contador_i + 1
            
            a0 = (x2_sum*yt_sum-x_sum*xy_sum)/(n*x2_sum-x_sum**2)
            a1 = (n*xy_sum-x_sum*yt_sum)/(n*x2_sum-x_sum**2)
            contador_i = 0 
            while contador_i <= (len(self.cor_x)-1):
                yma0ma1x_2 = (yt[contador_i]-a0-a1*self.cor_x[contador_i])**2
                yma0ma1x_2_sum = yma0ma1x_2_sum + yma0ma1x_2
                contador_i = contador_i + 1 

            r2 = (YmYp_2_sum-yma0ma1x_2_sum)/YmYp_2_sum
            print("\nMetodo Exponencial")
            print(f'r^2: {r2}')
            print(f'a0:  {a0}')
            print(f'a1:  {a1}')
            self.T.delete("1.0",tk.END)
            self.T.insert(END,"*-*-*-*-* Metodo Exponencial *-*-*-*-*\n")
            self.T.insert(END,f" a0  = {a0}\n a1  = {a1}\n r^2 = {r2}\n")
            self.T.insert(END,f" y = {math.e**a0}*e^({a1}*x)\n")
        except:
            print("Ingresar puntos nuevos")
    def Potencias(self):
        self.cor_x[:],self.cor_y[:] = [],[]
        try:
            contador_i = 0 
            x_y = "x"
            while contador_i < len(self.Puntos):
                if x_y == "x":
                    self.cor_x.append(float(self.Puntos[contador_i]))
                    x_y = "y"
                else:
                    self.cor_y.append(float(self.Puntos[contador_i]))
                    x_y = "x"
                contador_i = contador_i + 1
            #print(f"\n\n{self.Puntos}\n{self.cor_x}\n{self.cor_y}")
            
            n = len(self.cor_x)
            x2,y2 = 0,0
            r2 = 0
            xt,yt = [],[]
            contador_i = 0
            while contador_i < len(self.cor_x):
                xt_temp = math.log10(self.cor_x[contador_i])
                print('bandera 1')
                xt.append(xt_temp)

                yt_temp = math.log10(self.cor_y[contador_i])
                yt.append(yt_temp)
                contador_i = contador_i + 1
            
            # ------------ Proceso de calculo ----------------------
            xt_sum,yt_sum = 0,0
            x2_sum,y2_sum,xy_sum,YmYp_2_sum = 0,0,0,0
            yma0ma1x_2_sum = 0
            contador_i = 0
            while contador_i <= (len(self.cor_x)-1):
                xt_sum = xt_sum + xt[contador_i]
                yt_sum = yt_sum + yt[contador_i]
                contador_i = contador_i+1

            yp = yt_sum/n

            contador_i = 0
            while contador_i <= (len(self.cor_x)-1):
                x2 = (xt[contador_i])**2
                y2 = (yt[contador_i])**2
                xy = xt[contador_i]*yt[contador_i]
                YmYp_2 = (yt[contador_i]-yp)**2       # (y - yp)^2   

                x2_sum = x2_sum + x2
                y2_sum = y2_sum + y2
                xy_sum = xy_sum + xy
                YmYp_2_sum = YmYp_2_sum + YmYp_2

                contador_i = contador_i + 1
            
            a0 = (x2_sum*yt_sum-xt_sum*xy_sum)/(n*x2_sum-xt_sum**2)
            a1 = (n*xy_sum-xt_sum*yt_sum)/(n*x2_sum-xt_sum**2)
            contador_i = 0 
            while contador_i <= (len(self.cor_x)-1):
                yma0ma1x_2 = (yt[contador_i]-a0-a1*xt[contador_i])**2
                yma0ma1x_2_sum = yma0ma1x_2_sum + yma0ma1x_2
                contador_i = contador_i + 1 

            r2 = (YmYp_2_sum-yma0ma1x_2_sum)/YmYp_2_sum
            print("\nMetodo Potencias")
            print(f'r^2: {r2}')
            print(f'a0:  {a0}')
            print(f'a1:  {a1}')
            self.T.delete("1.0",tk.END)
            self.T.insert(END,"*-*-*-*-* Metodo Potencias *-*-*-*-*\n")
            self.T.insert(END,f" a0  = {a0}\n a1  = {a1}\n r^2 = {r2}\n")
            self.T.insert(END,f" y = {math.e**a0}*x^({a1}*x)\n")
        except:
            print("Ingresar puntos nuevos")

    def Saturacion(self):
        self.cor_x[:],self.cor_y[:] = [],[]
        try:
            contador_i = 0 
            x_y = "x"
            while contador_i < len(self.Puntos):
                if x_y == "x":
                    self.cor_x.append(float(self.Puntos[contador_i]))
                    x_y = "y"
                else:
                    self.cor_y.append(float(self.Puntos[contador_i]))
                    x_y = "x"
                contador_i = contador_i + 1
            #print(f"\n\n{self.Puntos}\n{self.cor_x}\n{self.cor_y}")
            n = len(self.cor_x)
            x2,y2 = 0,0
            xt,yt = [],[]
            r2 = 0
            contador_i = 0
            while contador_i < len(self.cor_x):
                xt_temp = 1/(self.cor_x[contador_i])
                xt.append(xt_temp)

                yt_temp = 1/(self.cor_y[contador_i])
                yt.append(yt_temp)
                contador_i = contador_i + 1

            # ------------ Proceso de calculo ----------------------
            xt_sum,yt_sum = 0,0
            x2_sum,y2_sum,xy_sum,YmYp_2_sum = 0,0,0,0
            yma0ma1x_2_sum = 0
            contador_i = 0
            while contador_i <= (len(self.cor_x)-1):
                xt_sum = xt_sum + xt[contador_i]
                yt_sum = yt_sum + yt[contador_i]
                contador_i = contador_i+1

            yp = yt_sum/n

            contador_i = 0
            while contador_i <= (len(self.cor_x)-1):
                x2 = (xt[contador_i])**2
                y2 = (yt[contador_i])**2
                xy = xt[contador_i]*yt[contador_i]
                YmYp_2 = (yt[contador_i]-yp)**2       # (y - yp)^2   

                x2_sum = x2_sum + x2
                y2_sum = y2_sum + y2
                xy_sum = xy_sum + xy
                YmYp_2_sum = YmYp_2_sum + YmYp_2

                contador_i = contador_i + 1
            
            a0 = (x2_sum*yt_sum-xt_sum*xy_sum)/(n*x2_sum-xt_sum**2)
            a1 = (n*xy_sum-xt_sum*yt_sum)/(n*x2_sum-xt_sum**2)
            contador_i = 0 
            while contador_i <= (len(self.cor_x)-1):
                yma0ma1x_2 = (yt[contador_i]-a0-a1*xt[contador_i])**2
                yma0ma1x_2_sum = yma0ma1x_2_sum + yma0ma1x_2
                contador_i = contador_i + 1 

            r2 = (YmYp_2_sum-yma0ma1x_2_sum)/YmYp_2_sum    
            print("\nMetodo Saturacion")    
            print(f'r^2: {r2}')
            print(f'a0:  {a0}')
            print(f'a1:  {a1}')
            self.T.delete("1.0",tk.END)
            self.T.insert(END,"*-*-*-*-* Metodo Saturación *-*-*-*-*\n")
            self.T.insert(END,f" a0  = {a0}\n a1  = {a1}\n r^2 = {r2}\n")
            self.T.insert(END,f" y = x/({a1}+{a0}*x)\n")
        except:
            print("Ingresar puntos nuevos")

    def Inter_Lagrange(self):
        self.cor_x[:],self.cor_y[:] = [],[]
        contador_i = 0 
        x_y = "x"
        temp_x, temp_y = [],[]
        while contador_i < len(self.Puntos):
            if x_y == "x":
                temp_x.append(float(self.Puntos[contador_i]))
                x_y = "y"
            else:
                temp_y.append(float(self.Puntos[contador_i]))
                x_y = "x"
            contador_i = contador_i + 1
        #print(f"\n\n{self.Puntos}\n{self.cor_x}\n{self.cor_y}")
        cant_puntos = len(temp_x)
        self.cor_x.append(temp_x[0])
        self.cor_x.append(temp_x[int((cant_puntos-1)*0.35)])
        self.cor_x.append(temp_x[int((cant_puntos-1)*0.65)])
        self.cor_x.append(temp_x[cant_puntos-1])
        
        self.cor_y.append(temp_y[0])
        self.cor_y.append(temp_y[int((cant_puntos-1)*0.35)])
        self.cor_y.append(temp_y[int((cant_puntos-1)*0.65)])
        self.cor_y.append(temp_y[cant_puntos-1])
        print(f"x= {self.cor_x},\ny= {self.cor_y}")



        # PROCEDIMIENTO
        # Polinomio de Lagrange
        n = len(self.cor_x)
        x = sym.Symbol('x')
        polinomio = 0
        divisorL = np.zeros(n, dtype = float)
        for i in range(0,n,1):
            # Termino de Lagrange
            numerador = 1
            denominador = 1
            for j  in range(0,n,1):
                if (j!=i):
                    numerador = numerador*(x-self.cor_x[j])
                    denominador = denominador*(self.cor_x[i]-self.cor_x[j])
            terminoLi = numerador/denominador

            polinomio = polinomio + terminoLi*self.cor_y[i]
            divisorL[i] = denominador

        # simplifica el polinomio
        polisimple = polinomio.expand()
        polisimple_str = "y = " + str(polisimple)

        # para evaluación numérica
        px = sym.lambdify(x,polisimple)

        # Puntos para la gráfica
        muestras = 100
        a = np.min(self.cor_x)
        b = np.max(self.cor_x)
        pxi = np.linspace(a,b,muestras)
        pfi = px(pxi)
        print(polisimple_str)
        self.T.delete("1.0",tk.END)
        self.T.insert(END,"*-*-*-*-* Interpolación de Lagrange *-*-*-*-*\n")
        self.T.insert(END,f" y  = {polisimple}\n")
            

        
if __name__ == "__main__":
    app = Proyecto()
    app.mainloop()