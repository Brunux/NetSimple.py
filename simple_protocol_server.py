#!/usr/bin/env python

# Example of protocol implementation
# simple_protocol_server.py
# Author: Bruno Fosados - bruno.fosados at gmail dot com

import socket
import random
import datetime # datetime.datetime.now()
import pdb

#Este es el "Header del protocolo"

SERVER_IP = '' # Vacio para escuchar en todas las interfaces
SERVER_PORT = 180
MAGIC_STR = "IFT" 
MAX_STR_SIZE = 1024 # El buffer
COOKIE1 = random.randint(1, 100)
COOKIE2 = random.randint(1, 100)
BYE_COMMENT = "Adios!"


#Implementacion del protocolo

def protocol(stream, data, address, COOKIE1, COOKIE2):
    '''
    TIPOS DE MENSAJES: HELLO, STATUS, BYE, BYE_CONFIRM
    Sintaxis:
        HELLO: "MAGIC_STR HELLO CARGA"
        STATUS: "MAGIC_STR STATUS COOKIE1 COOKIE2 IP:Port"
        BYE: "MAGIC_STR BYE SUMA_DE_COOKIES COMENTARIO"
        BYE_CONFIRM: "MAGIC_STR BYE_CONFIRM"
    '''
    if data[1] == 'HELLO':
        print "Server: HELLO recibido de:", address, datetime.datetime.now()
        status = send_hello(data, address, COOKIE1, COOKIE2)
        stream.send(status)
        return True

    elif data[1] == 'BYE' and data[2] == str(COOKIE1 + COOKIE2):
        print "Server: BYE recibido de:", address, datetime.datetime.now()
        bye_confirm = send_bye_confirm()
        stream.send(bye_confirm)
        return False

    else:
        stream.send("Paramentro no reconocido")
        return False

def send_hello(data, address, COOKIE1, COOKIE2):
    hello_load = data[2]
    print hello_load
    hello_response = MAGIC_STR + ' STATUS ' + str(COOKIE1) + ' ' + str(COOKIE2) + ' ' + str(address[0]) + ':' + str(address[1]) + ' ' + hello_load
    return hello_response

def send_bye_confirm():
    bye_confirm_response = MAGIC_STR + ' BYE_CONFIRM '
    return bye_confirm_response

#Creamos socket 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP,SERVER_PORT))
server_socket.listen(1)

#Creamos el stream de flujo y la direccion asociada con el cliente.
stream, address = server_socket.accept()
print "Server: conexion recibidad de: ", address, datetime.datetime.now()

while True:
    data = stream.recv(MAX_STR_SIZE)
    data_splited = data.split(" ")
    if data_splited[0] == MAGIC_STR:
        mantain_conection = protocol(stream, data_splited, address, COOKIE1, COOKIE2)
        if not mantain_conection:
            stream.close()
            print "Server: Cerrando Stream normalmente"
            break
    else:
        stream.send("No dijiste la palabra magica")
        stream.close()
        print "Server: Cerrando Stream se recibio la palabra Magica:", data_splited[0]
        raise ValueError("No Magic String")

print "Servidor: Saliendo...", datetime.datetime.now()
