from machine import Pin 
from machine import ADC #ADC hace que la rasberry tenga pines que reciban datos analogicos
from machine import PWM #PWM permite generar señales digitales periódicas (ondas cuadradas) para simular salidas analógicas
import time #Se importa para hacer pausas entre instrucciones con el comando .sleep

#Se definen los pines que controlan los segmentos del 7 segmentos
#Se tomo como ayuda para las conecciones el siguiente video: https://www.youtube.com/shorts/hsIBrn8cW7w
e  = Pin(13, Pin.OUT)
d  = Pin(14, Pin.OUT)
c  = Pin(15, Pin.OUT)
b  = Pin(16, Pin.OUT)
a  = Pin(17, Pin.OUT)
f  = Pin(18, Pin.OUT)
g  = Pin(19, Pin.OUT)

#Se agrega el pin del potenciometro (Con la configuracion ed ADC para que reciba señales analogicas
# y no es necesario poner Pin.IN ya que por default se entiene que solo va a recibir, no dar señales) 
poten = ADC(27)

#Se agrega el boton que le enviara la señal al servo para que haga el ciclo de 0 grados a 180
boton_servo = Pin(2, Pin.IN, Pin.PULL_DOWN)

#Para el funcionamiento del servomotor se uso como referencia el video: https://www.youtube.com/watch?v=r2YIaBHjj0g
servo =  PWM(Pin(28)) #Por la naturaleza del PWM no es necesario el Pin.OUT
servo.freq(50) #el 50 son l os hz en los que opera el servo motor
v_0_grados = 500000 #Por el ciclo del servo, girara 500k nanosegundos hacia 0 grados
v_180_grados = 2500000# Los 2.5 millones de nanosegundos representan un giro de 180

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
#======================================================
#Para el funcionamiento del potenciometro se uso como referencia el siguiente video: https://www.youtube.com/watch?v=IkbVy6IKhzU
#Loop que toma constantemente el valor del potenciometro y lo asigna a un numero del 1 al 3 en el 7 segmentos dependiendo en el intervalo en el que este
#Loop de prueba
while True:
    lectura = poten.read_u16() #Variable que toma el valor del potenciometro
    print(lectura)
    time.sleep_ms(500)
    if lectura < 43700 and lectura >= 21880:
        apagado()
        leer_numeros(2)
    elif lectura < 21880:
        apagado()
        leer_numeros(1)
    else:
        apagado()
        leer_numeros(3)
        
    if boton_servo.value() == 1:
        mover_servo()
#=============================================================================================================


