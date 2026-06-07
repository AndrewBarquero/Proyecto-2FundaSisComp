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

# CONFIGURACIoN DE RED
#la ip cambia, es importante poner la ip que te da la raspberry
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

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Se decalra la variable para abreviar las conexiones

def connect(): #funcion que conecta el micropy con py
    try: #Intenta enlazar la conexión.
        client_socket.connect((SERVER_IP, PORT)) #comprueba la conexión por medio de ip de server y puerto
        threading.Thread(target=receive_messages, daemon=True).start()
        print("Conectado al servidor") #una vez se enlaza, envia un mensaje de exito
    except Exception as e:
        print(f"Error de conexión: {e}") #Envía un mensaje de error si la conexión falla

def enviar_comando(msg): #función que permite enviar un comando a la rasp, ejecutando una función en la misma
    try:
        client_socket.send(msg.encode())
        print(f"Enviado: {msg}") #Intenta enviar el comando, si se envía con éxito, notifica con un mensaje
    except:
        print("No hay conexión con la Raspberry") #Si falla, despliega un mensaje de error

def receive_messages(): #funcion para que el py reciba mensajes y comandos de la rasp
    while True:
        try:
            msg = client_socket.recv(1024).decode() #intenta recibir el mensaje
            print(f"Raspberry: {msg}") #en caso de recibirlo, activa el comando y hace un print con el mensaje
        except:
            break #En caso contrario, rompe la iteración


def toggle_mantenimiento(): #función que activa y desactiva el modo mantenimiento.
    global en_mantenimiento

    if not en_mantenimiento:
        enviar_comando("MANTENIMIENTO_ON") #if que declara cuando se activa el modo mantenimiento y envia el comando a la rasp
        en_mantenimiento = True #Cambia a true el mantenimiento para alterar el estado de la máquina
        estado_label.config(text="ESTADO: MANTENIMIENTO ACTIVO", fg="red") #Despliega un texto que refleja el estado activo del mantenimiento
        boton_toggle.config(text="Desactivar mantenimiento", bg="red") #Establece un botón para desactivar el modo mantenimiento.
    else:
        enviar_comando("MANTENIMIENTO_OFF") #else que declara cuando se activa el modo mantenimiento y envia el comando a la rasp
        en_mantenimiento = False #Cambia a false el mantenimiento para alterar el estado de la máquina
        estado_label.config(text="ESTADO: VENTAS ACTIVAS", fg="green") #Despliega un texto que refleja el estado activo del mantenimiento
        boton_toggle.config(text="Activar mantenimiento", bg="green") #Establece un botón para activar el modo mantenimiento.

def abrir_ventana_mantenimiento(): #función para abrir la ventana mantenimiento
    ventana = tk.Toplevel() #Crea la ventana
    ventana.geometry("400x300") #Da dimensiones a la ventana
    ventana.title("Mantenimiento") #Da nombre a la ventana
    ventana.resizable(False, False) #No permite que cambie el tamaño de la ventana

    tk.Label( #Crea un texto indicando el modo de la ventana.
        ventana,
        text="MODO MANTENIMIENTO",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    global estado_label
    estado_label = tk.Label( #Crea un label que refleja el estado de operación normal
        ventana,
        text="ESTADO: VENTAS",
        fg="green",
        font=("Arial", 12)
    )
    estado_label.pack(pady=10)

    global boton_toggle
    boton_toggle = tk.Button( #Crea el botón en la ventana de mantenimiento para activarlo
        ventana,
        text="Activar mantenimiento", #Texto del botón
        width=25, #dimensiones y colores del botón
        height=2,
        bg="green",
        fg="white",
        command=toggle_mantenimiento #Comando que activa el botón.
    )
    boton_toggle.pack(pady=30)

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
            abrir_ventana_mantenimiento() #y abra la ventana de mantenimiento
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

ventana_principal = tk.Tk() #Se crea la ventana
ventana_principal.geometry("625x640+750+250") #Define las dimensiones de la ventana
ventana_principal.title("Maquina Expendedora") #Le asigna un titulo a la ventana
ventana_principal.resizable(False, False) #Hace que no se pueda cambiar el tamaño de la ventana

imagen_inicio = Image.open("Imagenes/Panel_principal.PNG") #Abre la ruta de la imagen
imagen_tk = ImageTk.PhotoImage(imagen_inicio)   #Trae la imagen abierta 
imagen_Pantalla_inicio = tk.Label(ventana_principal, image=imagen_tk) #Le asigna un label a la imagen
imagen_Pantalla_inicio.pack() #Coloca el label en la ventana



boton_mantenimiento = tk.Button(imagen_Pantalla_inicio, width=12,
                        relief="groove",bd=5, bg="#383447", #Se declara el tamaño, posición y colores del botón.
                        fg="White", text="Mantenimiento", #Se declara el texto que poseerá el botón y su color.
                        command= pedir_contrasena_mantenimiento) #Se declara el comando a ejecutar al presionar.
boton_mantenimiento.place(relx= 0.685, rely=0.565) #Se le da un espacio al botón


boton_estadistica = tk.Button(imagen_Pantalla_inicio, width=6,
                        relief="groove",bd=5, bg="#383447", #Se declara el tamaño, posición y colores del botón.
                        fg="White", text="Datos", #Se declara el texto que poseerá el botón y su color.
                        command= ventana_principal.destroy).place(relx= 0.67, rely=0.625) #Se declara el comando a ejecutar al presionar.

boton_salir = tk.Button(imagen_Pantalla_inicio, width=6,
                        relief="groove",bd=5, bg="#383447", #Se declara el tamaño, posición y colores del botón.
                        fg="white", text="Salir", #Se declara el texto que poseerá el botón y su color.
                        command=ventana_principal.destroy).place(relx= 0.78, rely=0.625) #Se declara el comando a ejecutar al presionar.


ventana_principal.protocol("WM_DELETE_WINDOW", ventana_principal.destroy)

connect()

ventana_principal.mainloop() #Se mantiene la ventana creada abierta


