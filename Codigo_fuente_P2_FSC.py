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

#El codigo que se usa para hacer la conexion camputadora-rasberry fue proporcionado por el profesor Luis Barboza. Todos los creditos a él.
#Solo se hicieron modificaciones a su codigo
#=====================Aqui se pondra el codigo para conectar la interfaz con la rasberry===================================

# CONFIGURACIoN DE RED
#la ip cambia, es importante poner la ip que te da la rasberry
SERVER_IP = '10.215.141.165'
# puerto de comunicacion
# ambos programas deben usar el MISMO puerto
PORT = 1717

# CREAR SOCKET CLIENTE:
# AF_INET:
# usar IPv4
#
# SOCK_STREAM:
# usar TCP
#
# TCP:
# conexion estable y segura
# parecida a una llamada telefonica
# ============================================================

client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)
#Funcion que se conecta al servidor
def connect():
    try:
        #Intenta conectarse a la rasberry
        client_socket.connect((SERVER_IP, PORT))
        # CREAR HILO PARA RECIBIR MENSAJES:
        # daemon=True:
        # el hilo se cerrara automaticamente
        # cuando cierre el programa
        threading.Thread(
            target=receive_messages,
            daemon=True
        ).start()

        print("Conectado al servidor")

    except Exception as e:
        # mostrar error si falla conexion
        print(f"Error: {e}")

#Funcion que envia un mensaje a la rasberry
def send_message():
    print("Hola")
    # obtener texto escrito en Entry
    msg = "Este mensaje es para la rasberry"

    # verificar que no este vacio
    if msg != "":
        # ENVIAR MENSAJE:
        # encode():
        # convierte texto a bytes
        # internet trabaja con bytes
        client_socket.send(msg.encode()) #esta linea es la que envia el mensaje a la rasberry
        print("se ha enviado el mensaje")

#Funcion que recibe mensajes de la rasberry
def receive_messages():
    while True:
        #Prueba si hay hay algun mensaje que recibir, si no, cierra el loop
        try:
            # RECIBIR DATOS
            # 1024:maximo de bytes a recibir
            msg = client_socket.recv(1024).decode()
            #Imprime el mensaje que recibe
            print(f"Raspberry: {msg}\n")
        except:
            break

#Funcion que termina la conexion en caso de que se cierre el programa
def salir():
    #Prueba si se puede cerrar, si no se puede es porque yano esta abierto y pasa
    try:
        # cerrar socket
        client_socket.close()
    except:
        pass
    ventana_principal.destroy()


#Iniciar la conexion
connect()

#==========       ============          ==============         ===========     ==============      =======================


ventana_principal = tk.Tk() #Se crea la ventana
ventana_principal.geometry("625x640+750+250") #Define las dimensiones de la ventana
ventana_principal.title("Maquina Expendedora") #Le asigna un titulo a la ventana
ventana_principal.resizable(False, False) #Hace que no se pueda cambiar el tmañana de la ventana

imagen_inicio = Image.open("Imagenes/Panel_principal.PNG") #Abre la ruta de la imagen
imagen_tk = ImageTk.PhotoImage(imagen_inicio)   #Trae la imagen abierta 
imagen_Pantalla_inicio = tk.Label(ventana_principal, image=imagen_tk) #Le asigna un label a la imagen
imagen_Pantalla_inicio.pack() #Coloca el label en la entana

tk.Label(imagen_Pantalla_inicio, text="PROYECTO #2 \n FSC\nAndrew Barquero\n Guillermo Mora", 
         bg="#445a4e", fg="#cef3c4", justify="center",
        font=("Arial", 13, "bold")).place(relx=0.67, rely=0.1)


boton_mantenimiento = tk.Button(imagen_Pantalla_inicio, width=12, 
                        relief="groove",bd=5, bg="#383447", 
                        fg="White", text="Mantenimiento", 
                        command=ventana_principal.destroy).place(relx= 0.685, rely=0.565)
boton_estadistica = tk.Button(imagen_Pantalla_inicio, width=6, 
                        relief="groove",bd=5, bg="#383447", 
                        fg="White", text="Datos", 
                        command=send_message).place(relx= 0.67, rely=0.625)
boton_salir = tk.Button(imagen_Pantalla_inicio, width=6, 
                        relief="groove",bd=5, bg="#383447", 
                        fg="white", text="Salir", 
                        command=salir).place(relx= 0.78, rely=0.625)
ventana_principal.protocol("WM_DELETE_WINDOW", ventana_principal.destroy)

ventana_principal.mainloop() #Se mantiene la ventana creada abierta


