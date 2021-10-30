import socket
import sys
#check open ports windows terminal: netstat -ab
HOST = '192.168.0.16' #ip robot 192.168.0.16
PORT = 30003 #cambiar al puerto que esté configurado el robot
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')
# s.bind((HOST,PORT))
s.connect((HOST, PORT))
# try:
#     s.bind((HOST, PORT))
# except socket.error as msg:
#     print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
#     sys.exit()
print ('Socket bind complete')
print ('Socket connection complete')
cmd = 'set_digital_out(3,True)' + "\n"
#cmd = "set_digital_out(2,False)" + "\n"
s.send(cmd.encode('utf-8'))
data = s.recv(1024)
s.close()
print("received", repr(data)) #repr representa en script los datos
# print("datos: ", data.decode("utf-8"))
