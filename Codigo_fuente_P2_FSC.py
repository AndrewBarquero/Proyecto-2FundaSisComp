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
"importé una libreria para poder meter la api del tipo de cambio"
import requests  # para consumir la API de tipo de cambio

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


CLAVE_ADMIN = "1234" #contraseña para ingresar al modo de mantenimiento
en_mantenimiento = False #declara cuando la máquina está en mantenimiento o no.

"agregué el precio en colones de los productos"

PRECIOS_COLONES = { #variables con los prefcios de los productos
    "X": 500,
    "Y": 750,
    "Z": 1000
}
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
            bg="green",
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
            bg="red",
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
def obtener_tipo_cambio(): #Funcion para obtener el tipo de cambio
    try:
        url = "https://open.er-api.com/v6/latest/USD" #Utiliza el link para actualizar el tipo de cambio del dolar en tiempo real
        respuesta = requests.get(url, timeout=5) #declara la variable respuesta para abreviar
        datos = respuesta.json() #guarda los resultados en un .json

        if datos["result"] == "success": #Cuando obtiene los resultados entra en estado de éxito
            return datos["rates"]["CRC"] #Y retorna el tipo de cambio
        else:
            return None
    except Exception as e:
        print("Error tipo de cambio:", e) #cuando no logra consultar el tipo de cambio, indica por medio de un mensaje, el error
        return None

def leer_ventas(): #función para leer la cantidad de ventas y
    try:
        with open("Estadisticas.txt", "r") as archivo: #abre un txt, como archivo para guardar y leer las ventas
            linea = archivo.readline().strip() #Crea una linea de texto para poder escribir

        if not linea: #si no hay linea no rfetorna nada
            return None

        # Formato esperado: [x,y,z]
        linea = linea.replace("[", "").replace("]", "") #se genera una lista para tener un formato en la linea creada
        partes = linea.split(",") #Separa por comaws los elementos de la lista

        if len(partes) != 3: #se encarga de que, al detectar más de trees elementos dentro de la lista, no retorne nada
            return None

        x = int(partes[0]) #Declara el espacio que ocupará cada producto en la lista.
        y = int(partes[1])
        z = int(partes[2])

        return x, y, z

    except Exception as e: #cuando no encuentre una estadística, entra en error, para la lectura e indica el error
        print("Error leyendo Estadisticas.txt:", e)
        return None

"cambié casi toda la función de estadística, partiendo de las bases que habian para poder implementar correctamente el tipo de cambio"

def estadistica(): #función de estadísticas.
    ventana_principal.withdraw() #Oculta la ventana principal completamente.

    ventana_datos = tk.Toplevel(ventana_principal) #Crea la ventana de datos
    ventana_datos.geometry("500x400+750+250") #le brinda dimensiones a la ventana
    ventana_datos.title("Estadísticas") #le agrega un nombre a la ventana
    ventana_datos.resizable(False, False) #hace que no se pueda editar el tamaño de la ventana

    contenedor = tk.LabelFrame(
        ventana_datos,
        text="Estadísticas de ventas" #pone un texto en la ventana.
    )
    contenedor.pack(padx=10, pady=10)

    # ===== UNIDADES VENDIDAS =====
    frame_ventas = tk.LabelFrame(contenedor, text="Unidades vendidas")
    frame_ventas.pack(side="left", padx=10, pady=10) #genera un texto directamente en la ventana.

    cantidad_ventas = tk.Text(frame_ventas, height=12, width=25)
    cantidad_ventas.pack() #crea un cuadro de texto en la ventana

    # ===== GANANCIAS =====
    frame_ganancias = tk.LabelFrame(contenedor, text="Ganancias")
    frame_ganancias.pack(side="right", padx=10, pady=10) #pone un texto en la ventana directamente, de ganancias

    dinero_ganado = tk.Text(frame_ganancias, height=12, width=25)
    dinero_ganado.pack() #crea un cuadro de texto en la ventana

    # ===== LEER DATOS =====
    datos = leer_ventas() #se llama a la función de leer ventas para calcular ganancias

    if not datos:
        cantidad_ventas.insert(tk.END, "No hay datos de ventas\n") #si no hay datos, indica que no encontró ninguno.
        dinero_ganado.insert(tk.END, "No hay datos de ventas\n")
    else:
        x, y, z = datos

        # ---- Mostrar ventas ----
        cantidad_ventas.insert(tk.END, "==== Ventas ====\n\n") #en caso de encontrar datos, dentro del cuadro de texto genera las estadisticas
        cantidad_ventas.insert(tk.END, f"Producto X: {x}\n") #estadísticas por producto.
        cantidad_ventas.insert(tk.END, f"Producto Y: {y}\n")
        cantidad_ventas.insert(tk.END, f"Producto Z: {z}\n")
        cantidad_ventas.insert(tk.END, f"Total: {x + y + z}\n")

        # ---- Calcular ganancias ----
        total_colones = ( #variable con fórmula aritmética para calcular el total de las ganancias
                x * PRECIOS_COLONES["X"] +
                y * PRECIOS_COLONES["Y"] +
                z * PRECIOS_COLONES["Z"]
        )

        dinero_ganado.insert(tk.END, "==== Ganancias ====\n\n") #inserta el resultado en el apartado de ganancias

    tipo_cambio = obtener_tipo_cambio() #llama a la función de tipo de cambio para poder utilizarlo

    # ---- Ganancias por producto ----
    ganancia_x = x * PRECIOS_COLONES["X"] #calcula las ganancias por tipo de producto
    ganancia_y = y * PRECIOS_COLONES["Y"] #calcula las ganancias por tipo de producto
    ganancia_z = z * PRECIOS_COLONES["Z"] #calcula las ganancias por tipo de producto

    dinero_ganado.insert(tk.END, "Producto X:\n")
    dinero_ganado.insert(tk.END, f"  CRC: ₡{ganancia_x}\n") #inserta los datos en el cuadro de texto, brindando el total de ganancias por producto

    dinero_ganado.insert(tk.END, "Producto Y:\n")
    dinero_ganado.insert(tk.END, f"  CRC: ₡{ganancia_y}\n") #inserta los datos en el cuadro de texto, brindando el total de ganancias por producto

    dinero_ganado.insert(tk.END, "Producto Z:\n")
    dinero_ganado.insert(tk.END, f"  CRC: ₡{ganancia_z}\n") #inserta los datos en el cuadro de texto, brindando el total de ganancias por producto

    # ---- Conversión a dólares ----
    if tipo_cambio: #if que inserta el tipo de cambio en el cuadro de texto.
        dinero_ganado.insert(tk.END, "\n-- En dólares --\n") #inserta un texto que indica la moneda a la que se hace cambio

        dinero_ganado.insert(
            tk.END, f"Producto X: ${ganancia_x / tipo_cambio:.2f}\n" #indica la ganancia por tipo de producto en dólares
        )
        dinero_ganado.insert(
            tk.END, f"Producto Y: ${ganancia_y / tipo_cambio:.2f}\n" #indica la ganancia por tipo de producto en dólares
        )
        dinero_ganado.insert(
            tk.END, f"Producto Z: ${ganancia_z / tipo_cambio:.2f}\n" #indica la ganancia por tipo de producto en dólares
        )

        dinero_ganado.insert(tk.END, "\n------------------\n") #Se añade un separador para poder ingresar el total y el tipo de cambio
        dinero_ganado.insert(
            tk.END, f"Total CRC: ₡{total_colones}\n" #inserta el total en colones
        )
        dinero_ganado.insert(
            tk.END, f"Total USD: ${total_colones / tipo_cambio:.2f}\n" #inserta el total en dólares
        )
        dinero_ganado.insert(
            tk.END, f"Tipo de cambio: ₡{tipo_cambio:.2f} / USD\n" #brinda el tipo de cambio
        )
    else:
        dinero_ganado.insert( #en caso de no obtener el tipo de cambio, indica un error
            tk.END, "Error al obtener tipo de cambio\n"
        )

    # ===== BOTÓN VOLVER =====
    def volver_datos(): #se crea la función de volver, que devuelve a la ventana principal
        ventana_datos.destroy() #cierra la ventana de datos completamente
        ventana_principal.deiconify()

    ventana_datos.protocol("WM_DELETE_WINDOW", volver_datos) #destruye la ventana para que no quede abierta

    tk.Button(
        ventana_datos, #Botón para salir de la ventana de datos
        text="Volver",
        width=12,
        bg="#383447",
        fg="white",
        command=volver_datos
    ).pack(pady=15)

"De aquí en adelante no toqué nada más"

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


