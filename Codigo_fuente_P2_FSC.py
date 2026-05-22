#Aqui haremos el codigo fuente para el segundo proyecto de fundamentos de sistemas computacionales.
#======================================
#Maquina expendedora

#El codigo en python sera para las siguientes tareas:
#Administrador de la maquina dispensadora
    #Se tendra una aplicacion hecha en Python para administrar la maquina dispensadora. Las funciones seran las
    #siguientes:
        #1. Visualizar en tiempo real la cantidad de unidades disponibles por cada producto.
        #2. Pantalla de estadısticas: se tendran las siguientes estadisticas historicas de la maquina dispensadora:
            #(a) Cantidad de ventas por producto y en general.
            #(b) Ganancias en colones y dolares (usando API con tipo de cambio).
        #3. Poner la maquina en estado Mantenimiento. En este estado no se pueden comprar productos. Se debe
            #distinguir de alguna forma.
#======================================

import tkinter as tk #Libreria de python para hacer GUI
from PIL import Image, ImageTk
import socket  #Libreria para conectar la computadora a la rasberry por medio de internet 
import threading #Libreria para ejecutar 2 instrucciones a la vez
import time  #Libreria que se usa para hacer tiempos entre funciones 

ventana_principal = tk.Tk() #Se crea la ventana
ventana_principal.geometry("625x640+750+250") #Define las dimensiones de la ventana
ventana_principal.title("Maquina Expendedora") #Le asigna un titulo a la ventana
ventana_principal.resizable(False, False) #Hace que no se pueda cambiar el tmañana de la ventana

imagen_inicio = Image.open("Imagenes/Panel_principal.PNG") #Abre la ruta de la imagen
imagen_tk = ImageTk.PhotoImage(imagen_inicio)   #Trae la imagen abierta 
imagen_Pantalla_inicio = tk.Label(ventana_principal, image=imagen_tk) #Le asigna un label a la imagen
imagen_Pantalla_inicio.pack() #Coloca el label en la entana


boton_mantenimiento = tk.Button(imagen_Pantalla_inicio, width=12, 
                        relief="groove",bd=5, bg="#383447", 
                        fg="White", text="Mantenimiento", 
                        command=ventana_principal.destroy).place(relx= 0.685, rely=0.565)
boton_estadistica = tk.Button(imagen_Pantalla_inicio, width=6, 
                        relief="groove",bd=5, bg="#383447", 
                        fg="White", text="Datos", 
                        command=ventana_principal.destroy).place(relx= 0.67, rely=0.625)
boton_salir = tk.Button(imagen_Pantalla_inicio, width=6, 
                        relief="groove",bd=5, bg="#383447", 
                        fg="white", text="Salir", 
                        command=ventana_principal.destroy).place(relx= 0.78, rely=0.625)
ventana_principal.protocol("WM_DELETE_WINDOW", ventana_principal.destroy)

ventana_principal.mainloop() #Se mantiene la ventana creada abierta


