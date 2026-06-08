"""
from machine import Pin
import _thread #Hace que se puedan hacer mas de una tarea a la vez
import network #La libreria encargada de hacer que la raspy se pueda conectar
import socket #La libreria que conecta la raspy con otro dispositivo
from machine import ADC #ADC hace que la rasberry tenga pines que reciban datos analogicos
from machine import PWM #PWM permite generar señales digitales periódicas (ondas cuadradas) para simular salidas analógicas
import time #Se importa para hacer pausas entre instrucciones con el comando .sleep

#================Configuracion a internet==================
SSID     = "Andrew's phone"   # Nombre de la red WiFi
PASSWORD = "soypobre"         # Contraseña de la red
PORT     = 1717               # Puerto TCP del servidor

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    print("Conectando a WiFi...", end="")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)
    print("\nConectado:", wlan.ifconfig())
    return wlan.ifconfig()[0]

ip = connect_wifi()
conn 
def start_server():
    global ip
    s = socket.socket()
    s.bind((ip, 1717))
    s.listen(1)
    print("Esperando conexión del cliente...")
    conn, addr = s.accept()
    print("Conectado desde:", addr)

def recibir_mensaje():
    global conn
    while True:
        data = conn.recv(1024)
        if not data:
            break
        msg = data.decode()
        print("Mensaje recibido:", msg)
        
        # Acciones según el mensaje
        conn.send(f"Echo: {msg}".encode())

#====================================================


#Se definen los pines que controlan los segmentos del 7 segmentos
#Se tomo como ayuda para las conecciones el siguiente video: https://www.youtube.com/shorts/hsIBrn8cW7w
e  = Pin(13, Pin.OUT)
d  = Pin(14, Pin.OUT)
c  = Pin(15, Pin.OUT)
b  = Pin(16, Pin.OUT)
a  = Pin(17, Pin.OUT)
f  = Pin(18, Pin.OUT)
g  = Pin(19, Pin.OUT)

led_verde = Pin(12,Pin.OUT)
led_rojo =  Pin(11,Pin.OUT)

#Se agrega el pin del potenciometro (Con la configuracion ed ADC para que reciba señales analogicas
# y no es necesario poner Pin.IN ya que por default se entiene que solo va a recibir, no dar señales) 
poten = ADC(27)

#Se agrega el boton que le enviara la señal al servo para que haga el ciclo de 0 grados a 180
boton_servo = Pin(2, Pin.IN, Pin.PULL_DOWN)

#Para el funcionamiento del servomotor se uso como referencia el video: https://www.youtube.com/watch?v=r2YIaBHjj0g
servo =  PWM(Pin(28)) #Por la naturaleza del PWM no es necesario el Pin.OUT
servo.freq(50) #el 50 son l os hz en los que opera el servo motor
v_0_grados = 500000 #Por el ciclo del servo, girara 500k nanosegundos hacia 0 grados
v_180_grados = 2500000 # Los 2.5 millones de nanosegundos representan un giro de 180

#Funcion que hace que el motor del servomotor gire de 0 a 180 grados
def mover_servo():
    servo.duty_ns(v_0_grados) 
    time.sleep(5) #Aqui espera 5 segundos para que el usuario tenga el tiempo suficiente para obteer el producto
    servo.duty_ns(v_180_grados) 
    time.sleep(1)

    
#============Aqui esta el conjunto de funciones que muestran los diferentes numeros en el 7 segmentos=======
#Funcion que apaga todos los 7 segmentos; funciona para hacer pausas entre cambio de numeros
def apagado():
    a.value(0)
    b.value(0)
    c.value(0)
    d.value(0)
    e.value(0)
    f.value(0)
    g.value(0)

#diccionario donde se asignan los valores de los 7 segmentos que se deben encender para mostrar cada determinado numero
numeros = {0: "abcdef", 1: "bc", 2: "abged", 3: "abgcd" ,
           4: "fgbc", 5: "afgcd", 6: "afgecd", 7: "abc",
           8: "abcdefg" , 9: "abcfg"}

#Funcion que recibe un numero y recorre la cadena de letras que estan asignadas al numero para mostralo
def leer_numeros(num):
    for i in range(len(numeros[num])):
        if (numeros[num][i]) == "a":
            a.value(1)
        elif (numeros[num][i]) == "b":
            b.value(1)
        elif (numeros[num][i]) == "c":
            c.value(1)
        elif (numeros[num][i]) == "d":
            d.value(1)
        elif (numeros[num][i]) == "e":
            e.value(1)
        elif (numeros[num][i]) == "f":
            f.value(1)
        elif (numeros[num][i]) == "g":
            g.value(1)    

#Funcion que hace que el 7 segmentos muestre los numeros del 0 al 9 (funcion de prueba para verificar el buen funcionamiento del dispositivo)
def mostrar_numeros():
    for i in range(10):
        leer_numeros(i)
#=====================================================
#Las siguientes variables son la cantidad de los 3 productos que hay
cantidad_de_x_producto = 0
cantidad_de_y_producto = 3
cantidad_de_z_producto = 1

#Rangos de los valores del potenciometro para dividir el rango total del potenciometro
#Se le asigna un producto a cada rango
x = range(0,21880)
y = range(21880, 43700)
z = range(43700, 700000)

#Esta funcion se activa cuando se pulsa el boton y recibe la lectura del potenciometro, determina en que rango se esta y si el producto asociado es diferente de 0.
#si es diferente de 0, activa el servo motor y resta uno a la cantidad de producto
def interaccion_producto_maquina(num):
    global cantidad_de_x_producto, cantidad_de_y_producto, cantidad_de_z_producto #Para cambiar las variables de productos se llaman con global
    
    print(f"Hola, la lectura es {num}")
    if num in x: #Este if y los otros elif determinan en que rango se esta, para saber con que producto interactuar
        if cantidad_de_x_producto != 0: #Solo activa el servo si hay producto
            mover_servo()
            cantidad_de_x_producto -= 1
            conn.send(f"Se ha comprado del producto X".encode())
    elif num in y:
        if cantidad_de_y_producto != 0:
            mover_servo()
            cantidad_de_y_producto -= 1
            conn.send(f"Se ha comprado del producto Y".encode())
    elif num in z:
        if cantidad_de_z_producto != 0:
            mover_servo()
            cantidad_de_z_producto -= 1
            conn.send("Se ha comprado del producto Z".encode())

    
#======================================================
#Para el funcionamiento del potenciometro se uso como referencia el siguiente video: https://www.youtube.com/watch?v=IkbVy6IKhzU
#Loop que toma constantemente el valor del potenciometro y lo asigna a un numero del 1 al 3 en el 7 segmentos dependiendo en el intervalo en el que este
#Loop principal
_thread.start_new_thread(recibir_mensaje, ())
while True:
    lectura = poten.read_u16() #Variable que toma el valor del potenciometro
    #print(lectura)
    time.sleep_ms(100)
    if lectura in y:
        apagado()
        leer_numeros(cantidad_de_y_producto)
        if cantidad_de_y_producto == 0:
            led_verde.value(0)
            led_rojo.value(1)
        else:
            led_verde.value(1)
            led_rojo.value(0)
    elif lectura in x:
        apagado()
        leer_numeros(cantidad_de_x_producto)
        if cantidad_de_x_producto == 0:
            led_verde.value(0)
            led_rojo.value(1)
        else:
            led_verde.value(1)
            led_rojo.value(0)
    else:
        apagado()
        leer_numeros(cantidad_de_z_producto)
        if cantidad_de_z_producto == 0:
            led_verde.value(0)
            led_rojo.value(1)
        else:
            led_verde.value(1)
            led_rojo.value(0)
        
    time.sleep_ms(100)
    if boton_servo.value() == 1:
        interaccion_producto_maquina(lectura)
        
    time.sleep_ms(100)
    
#=============================================================================================================
"""

