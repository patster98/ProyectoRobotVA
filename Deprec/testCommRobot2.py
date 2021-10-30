# Test

import socket
#
import time
#
HOST = "192.168.0.16" # IP del robot

PORT = 30003 # port: 30001, 30002 o 30003, en ambos extremos (gripper 63352)
#
print("Conectando a IP: ", HOST)
#
#
#
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
print("conectando...")
#
s.connect((HOST, PORT))
#
time.sleep(0.5)
# comado = "movej(p[%f,%f,%f,1.0,20.0,0.0])/n)"
# comandoB=comado.encode("utf-8")
# s.send(comandoB)


print("El robot comienza a moverse con comandos de pose")

# s.send (b"movej(p[0.00, 0.3, 0.4, 2.22, -2.22, 0.00], a=1.0, v=0.1)\n")
#
# time.sleep(10) # este programa no sabe cuándo concluye el movimiento, espera 10s antes de iniciar el siguiente
#
# s.send (b"movej(p[0.00, 0.3, 0.3, 2.22, -2.22, 0.00], a=1.0, v=0.1)\n")
#
# time.sleep(10)
#
# s.send (b"movej(p[0.00, 0.3, 0.2, 2.22, -2.22, 0.00], a=1.0, v=0.1)\n")
#
# time.sleep(10)
#
# s.send(b"popup(Dale boquita, Rey de copas,blocking=True)\n")
# time.sleep(10)

print("prueba gripper")
# s.send(b"set_tool_digital_out(2,True)\n")
# time.sleep(5)
# s.send(b"set_tool_digital_out(2,False)\n")
# print("prueba 1")
# time.sleep(5)
s.send(b"set_standard_digital_out(2,True)\n")
time.sleep(5)
print("prueba 2")
s.send(b"set_standard_digital_out(2,False)\n")
time.sleep(5)




data = s.recv(1024)



s.close()

print("Recibido del robot: ", repr(data))