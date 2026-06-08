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
def enviar_comando():
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
#connect()
CLAVE_ADMIN = "1234" #contraseña para ingresar al modo de mantenimiento
en_mantenimiento = False #declara cuando la máquina está en mantenimiento o no.

#==========       ============          ==============         ===========     ==============      =======================
ventana_principal = tk.Tk() #Se crea la ventana
ventana_principal.geometry("625x640+750+250") #Define las dimensiones de la ventana
ventana_principal.title("Maquina Expendedora") #Le asigna un titulo a la ventana
ventana_principal.resizable(False, False) #Hace que no se pueda cambiar el tmañana de la ventana

imagen_inicio = Image.open("Imagenes/Panel_principal.PNG") #Abre la ruta de la imagen
imagen_tk = ImageTk.PhotoImage(imagen_inicio)   #Trae la imagen abierta 
imagen_Pantalla_inicio = tk.Label(ventana_principal, image=imagen_tk) #Le asigna un label a la imagen
imagen_Pantalla_inicio.pack() #Coloca el label en la entana

#Se crea una label como titulo de la interfaz
tk.Label(imagen_Pantalla_inicio, text="PROYECTO #2 \n FSC\nAndrew Barquero\n Guillermo Mora", 
         bg="#445a4e", fg="#cef3c4", justify="center",
        font=("Arial", 13, "bold")).place(relx=0.67, rely=0.1)

#========================================Ventanas de mantenimiento y datos=====================================
def toggle_mantenimiento(): #función que activa y desactiva el modo mantenimiento.
    global en_mantenimiento

    if not en_mantenimiento:
        #enviar_comando("MANTENIMIENTO_ON") #if que declara cuando se activa el modo mantenimiento y envia el comando a la rasp
        en_mantenimiento = True #Cambia a true el mantenimiento para alterar el estado de la máquina
        estado_label.config(text="ESTADO: MANTENIMIENTO ACTIVO", fg="red") #Despliega un texto que refleja el estado activo del mantenimiento
        boton_toggle.config(text="Desactivar mantenimiento", bg="green") #Establece un botón para activar el modo mantenimiento.
    else:
        #enviar_comando("MANTENIMIENTO_OFF") #else que declara cuando se activa el modo mantenimiento y envia el comando a la rasp
        en_mantenimiento = False #Cambia a false el mantenimiento para alterar el estado de la máquina
        estado_label.config(text="ESTADO: VENTAS ACTIVAS", fg="green") #Despliega un texto que refleja el estado activo del mantenimiento
        boton_toggle.config(text="Activar mantenimiento", bg="red") #Establece un botón para desactivar el modo mantenimiento.

def abrir_ventana_mantenimiento(): #función para abrir la ventana mantenimiento
    ventana_principal.withdraw()
    ventana_mantenimiento = tk.Toplevel() #Crea la ventana
    ventana_mantenimiento.geometry("400x300+750+250") #Da dimensiones a la ventana
    ventana_mantenimiento.title("Mantenimiento") #Da nombre a la ventana
    ventana_mantenimiento.resizable(False, False) #No permite que cambie el tamaño de la ventana

    tk.Label( #Crea un texto indicando el modo de la ventana.
        ventana_mantenimiento,
        text="MODO MANTENIMIENTO",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    global estado_label
    if not en_mantenimiento:
        estado_label = tk.Label( #Crea un label que refleja el estado de operación normal
            ventana_mantenimiento,
            text="ESTADO: VENTAS",
            fg="green",
            font=("Arial", 12)
        )
        estado_label.pack(pady=10)
    else:
        estado_label = tk.Label( #Crea un label que refleja el estado de operación normal
            ventana_mantenimiento,
            text="ESTADO: MANTENIMIENTO",
            fg="red",
            font=("Arial", 12)
        )
        estado_label.pack(pady=10)

    global boton_toggle
    if not en_mantenimiento:
        boton_toggle = tk.Button( #Crea el botón en la ventana de mantenimiento para activarlo
            ventana_mantenimiento,
            text="Activar mantenimiento", #Texto del botón
            width=25, #dimensiones y colores del botón
            height=2,
            bg="red",
            fg="white",
            command=toggle_mantenimiento #Comando que activa el botón.
        )
        boton_toggle.pack(pady=30)
    else:
        boton_toggle = tk.Button( #Crea el botón en la ventana de mantenimiento para activarlo
            ventana_mantenimiento,
            text="Desactivar mantenimiento", #Texto del botón
            width=25, #dimensiones y colores del botón
            height=2,
            bg="green",
            fg="white",
            command=toggle_mantenimiento #Comando que activa el botón.
        )
        boton_toggle.pack(pady=30)


    def volver_mantenimietno(): #Funcion que cierra la ventana
        ventana_mantenimiento.destroy() #destruye la ventana 
        ventana_principal.deiconify() #Vuelve a mostrar la ventana principal
    ventana_mantenimiento.protocol("WM_DELETE_WINDOW", salir)
    tk.Button(ventana_mantenimiento, width=11, 
            relief="groove",bd=5, bg="#383447", #Se declara el tamaño, posición y colores del botón.
            fg="White", text="Volver", command=volver_mantenimietno).pack(pady=30)

def pedir_contrasena_mantenimiento(): #función para pedir y validar la contraseña.
    ventana_pass = tk.Toplevel() #Crea la ventana.
    ventana_pass.geometry("350x200+750+250") #Le agrega dimensiones a la ventana
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
#====================================================Ventana de estadisticas=============================================================================================
def estadistica():
    ventana_principal.withdraw()
    ventana_datos = tk.Toplevel(ventana_principal)
    ventana_datos.geometry("500x400+750+250")
    ventana_datos.title("Estadisticas")
    ventana_datos.resizable(False, False)

    """
    Para escribir en el .txt
    with open("archivo.txt", "w") as archivo:
    archivo.write("")
    
    Lineas que abren el .txt y escriben ahi 
    with open("puntaje.txt", "a", encoding="utf-8") as f:
        f.write(f"{usuario}, {tiempo_transcurrido}\n")
    """
    def mostrar_cantidad_productos():
        try:
            archivo = open("Estadisticas.txt", "r")
        except:
            return [0,0,0]

        lista_ventas = archivo.readlines()
        archivo.close() 
        lista1 = lista_ventas[0]
        def str_list(lista):
            lista2= []
            for i in range(len(lista)):
                if lista[i] == "[":
                    i1 = i+1
                if lista[i] == "]":
                    i2 = i
            lista2 = lista[i1:i2]
            lista3 = []
            X,Y,Z = lista2.split(",")
            x = int(X)
            y = int(Y)
            z = int(Z)
            lista3 = lista3 +[x]+[y]+[z]
            return lista3
        lista1 = str_list(lista1)
        
        cantidad_ventas.delete("1.0", tk.END)
        cantidad_ventas.insert(tk.END, "==== Se ha vendido: ====\n\n")
        cantidad_ventas.insert(tk.END, f"Del producto X: {lista1[0]}\n")
        cantidad_ventas.insert(tk.END, f"Del producto Y: {lista1[1]}\n")
        cantidad_ventas.insert(tk.END, f"Del producto Z: {lista1[2]}\n")
        cantidad_ventas.insert(tk.END, f"En total: {sum(lista1)}\n")

        
    datos_label = tk.LabelFrame(ventana_datos, text="Estadistica de los productos vendidos")
    datos_label.pack()
    
    titulo_cantidad_ventas = tk.LabelFrame(datos_label, text="Unidades vendidas")
    titulo_cantidad_ventas.pack(side="left")

    cantidad_ventas = tk.Text(titulo_cantidad_ventas, height=10, width= 25)
    cantidad_ventas.pack()

    titulo_dinero_ganado = tk.LabelFrame(datos_label, text="Dinero ganado")
    titulo_dinero_ganado.pack(side="right")

    dinero_ganado = tk.Text(titulo_dinero_ganado, height=10, width= 25)
    dinero_ganado.pack()
    mostrar_cantidad_productos()

    def volver_datos(): #Funcion que cierra la ventana
        ventana_datos.destroy() #destruye la ventana 
        ventana_principal.deiconify() #Vuelve a mostrar la ventana principal
    ventana_datos.protocol("WM_DELETE_WINDOW", salir)
    tk.Button(ventana_datos, width=11, 
            relief="groove",bd=5, bg="#383447", #Se declara el tamaño, posición y colores del botón.
            fg="White", text="Volver", command=volver_datos).pack(pady=50)
#=====================================================================================================================================================================

boton_mantenimiento = tk.Button(imagen_Pantalla_inicio, width=12,
                        relief="groove",bd=5, bg="#383447", #Se declara el tamaño, posición y colores del botón.
                        fg="White", text="Mantenimiento", #Se declara el texto que poseerá el botón y su color.
                        command= pedir_contrasena_mantenimiento) #Se declara el comando a ejecutar al presionar.
boton_mantenimiento.place(relx= 0.685, rely=0.565) #Se le da un espacio al botón


boton_estadistica = tk.Button(imagen_Pantalla_inicio, width=6,
                        relief="groove",bd=5, bg="#383447", #Se declara el tamaño, posición y colores del botón.
                        fg="White", text="Datos", #Se declara el texto que poseerá el botón y su color.
                        command= estadistica).place(relx= 0.67, rely=0.625) #Se declara el comando a ejecutar al presionar.

boton_salir = tk.Button(imagen_Pantalla_inicio, width=6,
                        relief="groove",bd=5, bg="#383447", #Se declara el tamaño, posición y colores del botón.
                        fg="white", text="Salir", #Se declara el texto que poseerá el botón y su color.
                        command=ventana_principal.destroy).place(relx= 0.78, rely=0.625) #Se declara el comando a ejecutar al presionar.

#Esta linea hace que cuando se preciona la equis de la ventana, se ejecute el mismo proceso que el del boton de salir
ventana_principal.protocol("WM_DELETE_WINDOW", salir)

ventana_principal.mainloop() #Se mantiene la ventana creada abierta


