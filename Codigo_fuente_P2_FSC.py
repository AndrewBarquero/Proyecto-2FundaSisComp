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

CLAVE_ADMIN = "1234" #contraseña para ingresar al modo de mantenimiento
en_mantenimiento = False #declara cuando la máquina está en mantenimiento o no.

ventana_principal = tk.Tk() #Se crea la ventana
ventana_principal.geometry("625x640+750+250") #Define las dimensiones de la ventana
ventana_principal.title("Maquina Expendedora") #Le asigna un titulo a la ventana
ventana_principal.resizable(False, False) #Hace que no se pueda cambiar el tamaño de la ventana

imagen_inicio = Image.open("Imagenes/Panel_principal.PNG") #Abre la ruta de la imagen
imagen_tk = ImageTk.PhotoImage(imagen_inicio)   #Trae la imagen abierta 
imagen_Pantalla_inicio = tk.Label(ventana_principal, image=imagen_tk) #Le asigna un label a la imagen
imagen_Pantalla_inicio.pack() #Coloca el label en la ventana

def pedir_contrasena_mantenimiento(): #función para pedir y validar la contraseña.
    ventana_pass = tk.Toplevel() #Crea la ventana.
    ventana_pass.geometry("350x200") #Le agrega dimensiones a la ventana
    ventana_pass.title("Acceso restringido") #Le da un nombre a la ventana
    ventana_pass.resizable(False, False) #Hace que no pueda editarse el tamaño de la ventana

    tk.Label( #Agrega por medio de un label, una indicación al usuario.
        ventana_pass,
        text="Ingrese la contraseña de administrador", #Le indica el ingreso de la contraseña, el tipo de texto y el espacio en el cual desplegarse
        font=("Arial", 12)
    ).pack(pady=15)

    entrada_clave = tk.Entry(ventana_pass, show="*", width=25) #se declara una entrada, donde escribir que cifra la clave para que al digitarse no se muestre.
    entrada_clave.pack(pady=5) #Se le da un espacio en la ventana

    mensaje_error = tk.Label(ventana_pass, text="", fg="red") #se declara una variable a editar cuando se proceda a la validación. (Mensaje de error)
    mensaje_error.pack()

    def validar(): #función que valida correctamente la contraseña
        if entrada_clave.get() == CLAVE_ADMIN: #Declara una variable que al ser igual que la clave global
            ventana_pass.destroy() #destruya la ventana de contraseña
            abrir_ventana("Mantenimiento") #y abra la ventana de mantenimiento
        else:
            mensaje_error.config(text="Contraseña incorrecta") #en caso de ingresar erróneamente la contraseña, indica que la contraseña es incorrecta y no le deja ingresar

    tk.Button(
        ventana_pass,
        text="Ingresar", #Crea el boton para ingresar, que activa la validación.
        width=15,
        bg="#383447",
        fg="white",
        command=validar
    ).pack(pady=15)

def abrir_ventana(titulo): #Función para crear ventanas, con el parámetro del titulo.
    ventana = tk.Toplevel() #Declara la variable ventana como una ventana independiente de la principal
    ventana.geometry("400x300") #Define las dimensiones de la ventana
    ventana.title(titulo) #LLama al parámetro del título, que cambiará según el botón que se utilice, para nombrar a la nueva ventana creada

    tk.Label(
        ventana,
        text=f"Estás en: {titulo}", #Prueba para determinar que la ventana haya sido creada correctamente
        font=("Arial", 16)
    ).pack(pady=40)

boton_mantenimiento = tk.Button(imagen_Pantalla_inicio, width=12,
                        relief="groove",bd=5, bg="#383447", #Se declara el tamaño, posición y colores del botón.
                        fg="White", text="Mantenimiento", #Se declara el texto que poseerá el botón y su color.
                        command= pedir_contrasena_mantenimiento) #Se declara el comando a ejecutar al presionar.
boton_mantenimiento.place(relx= 0.685, rely=0.565) #Se le da un espacio al botón


boton_estadistica = tk.Button(imagen_Pantalla_inicio, width=6,
                        relief="groove",bd=5, bg="#383447", #Se declara el tamaño, posición y colores del botón.
                        fg="White", text="Datos", #Se declara el texto que poseerá el botón y su color.
                        command= lambda: abrir_ventana("Estadísticas")).place(relx= 0.67, rely=0.625) #Se declara el comando a ejecutar al presionar.

boton_salir = tk.Button(imagen_Pantalla_inicio, width=6,
                        relief="groove",bd=5, bg="#383447", #Se declara el tamaño, posición y colores del botón.
                        fg="white", text="Salir", #Se declara el texto que poseerá el botón y su color.
                        command=ventana_principal.destroy).place(relx= 0.78, rely=0.625) #Se declara el comando a ejecutar al presionar.


ventana_principal.protocol("WM_DELETE_WINDOW", ventana_principal.destroy)

ventana_principal.mainloop() #Se mantiene la ventana creada abierta


