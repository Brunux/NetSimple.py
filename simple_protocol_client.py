#!/usr/bin/env python

# Example of protocol implementation
# simple_protocol_client.py
# Author: Bruno Fosados - bruno.fosados at gmail dot com

import sys
import datetime # datetime.datetime.now()
import socket
import pdb


# Este es el "Header del protocolo"
SERVER_IP = '192.168.221.131'
SERVER_PORT = 180
MAGIC_STR = "MakeMagic"
MAX_STR_SIZE = 1024 # El buffer
LOAD = 'Carga_predeterminada'
BYE_COMMENT = "Adios!"
msg = ''

# Implementar usage: client [<hostname>[ <port>]] <carga>
if len(sys.argv) > 4 or len(sys.argv) < 2:
    print "usage: protocol_client [<hostname>[ <port>]] <carga>"
    exit()
else:
    if len(sys.argv) == 2 and sys.argv[1] != ' ':
        LOAD = sys.argv[1]
        print SERVER_IP, SERVER_PORT, LOAD
    elif len(sys.argv) == 3:
        SERVER_IP = sys.argv[1]
        SERVER_PORT = int(sys.argv[2]) # agregar un TRY: para verificar que se pueda convertir a INT
        print SERVER_IP, SERVER_PORT, LOAD
    elif sys.argv[1] != ' ' and sys.argv[2] != ' ' and sys.argv[3] != ' ':
        SERVER_IP = sys.argv[1]
        SERVER_PORT = int(sys.argv[2]) # agregar un TRY: para verificar que se pueda convertir a INT
        LOAD = sys.argv[3]
        print SERVER_IP, SERVER_PORT, LOAD
    else:
        print "usage: protocol_client [<hostname>[ <port>]] <carga>"
        exit()

# Implementacion del protocolo
def protocol(stream, data):
    '''
    TIPOS DE MENSAJES: HELLO, STATUS, BYE, BYE_CONFIRM
    Sintaxis:
        HELLO: "MAGIC_STR HELLO CARGA"
        STATUS: "MAGIC_STR STATUS COOKIE1 COOKIE2 IP:PORT"
        BYE: "MAGIC_STR BYE SUMA_DE_COOKIES COMENTARIO"
        BYE_CONFIRM: "MAGIC_STR BYE_CONFIRM"
    '''
    # Verificar de 'STATUS'
    if data[1] == 'STATUS' and int(data[4].split(":")[1]) == stream.getsockname()[1]:
        print "Cliente: STATUS recibido!" , data
        COOKIE1 = int(data[2])
        COOKIE2 = int(data[3])
        send_bye = bye(COOKIE1, COOKIE2)
        stream.send(send_bye)
        print "Cliente: Enviando 'BYE'"
        return True

    # Verificar de 'BYE_CONFIRM'
    elif data[1] == 'BYE_CONFIRM':
        print "Cliente: BYE_CONFIRM recibido!", data
        return False
    # Sino se reconoce el parametro regresamos false para cerrar la conexion
    else:
        print "Parametro no reconocido"
        return False

# Funcion para envio de HELLO
def hello(load):
    send_hello = MAGIC_STR + ' HELLO ' + load
    return send_hello

# Funcion para envio de BYE
def bye(COOKIE1, COOKIE2):
    cookie_sum = COOKIE1 + COOKIE2
    send_bye = MAGIC_STR + ' BYE ' + str(cookie_sum) + ' ' + BYE_COMMENT
    return send_bye

# Creamos socket 
stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectamos con el servidor
stream.connect((SERVER_IP, SERVER_PORT))

# Enviar HELLO
stream.send(hello(LOAD)) # Sacar hello_load de la linea de comandos
print "Cliente: Enviando 'HELLO'"

# Leer respuesta
while True:
    data = stream.recv(MAX_STR_SIZE)
    print "Cliente: se recibio esta data:", data
    data_splited = data.split(" ")
    # Verificar el Magic String y Lanzar la funcion de analizar el protocolo
    if data_splited[0] == MAGIC_STR:
        mantain_conection = protocol(stream, data_splited)
        # Sino se necesita manter el stream abierto lo cerramos
        if not mantain_conection:
            stream.close()
            print "Cerrando Stream normalmente..."
            break
    # Sino hay Magic String cerramos el stream y levantamos una exeption
    else:
        stream.send("No dijiste la palabra magica de forma correcta")
        stream.close()
        print "Cliente: Cerrando stream no se recibio la palabra magica de forma correcta", MAGIC_STR
        raise ValueError("No Magic String")

print "Cliente: Saliendo...", datetime.datetime.now()
