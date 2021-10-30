# Test

import socket

import time

HOST = "192.168.0.16" # IP del robot

PORT = 30001 # port: 30001, 30002 o 30003, en ambos extremos

print("Conectando a IP: ", HOST)



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("conectando...")

s.connect((HOST, PORT))

time.sleep(0.5)



print("El robot comienza a moverse con comandos de pose")

s.send (b"movej(p[0.00, 0.3, 0.4, 2.22, -2.22, 0.00], a=1.0, v=0.1)\n")

time.sleep(10) # este programa no sabe cuándo concluye el movimiento, espera 10s antes de iniciar el siguiente

s.send (b"movej(p[0.00, 0.3, 0.3, 2.22, -2.22, 0.00], a=1.0, v=0.1)\n")

time.sleep(10)

s.send (b"movej(p[0.00, 0.3, 0.2, 2.22, -2.22, 0.00], a=1.0, v=0.1)\n")

time.sleep(10)

data = s.recv(1024)



s.close()

print("Recibido del robot: ", repr(data))
