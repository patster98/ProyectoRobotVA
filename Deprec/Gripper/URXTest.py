import urx
import time
a = 1.0
v = 0.5
x=0.2
y=0.3
z= 0.4
rx= 0
ry= 0
rz= 3.14

rob = urx.Robot("192.168.0.16")
rob.set_tcp((0, 0, 0.1, 0, 0, 0))
rob.set_payload(2, (0, 0, 0.1))
time.sleep(0.2)  #leave some time to robot to process the setup commands
rob.movej((1, 2, 3, 4, 5, 6), a, v)
rob.movel((x, y, z, rx, ry, rz), a, v)
print( "Current tool pose is: ",  rob.getl())
rob.movel((0.1, 0, 0, 0, 0, 0), a, v, relative=true)  # move relative to current pose
rob.translate((0.1, 0, 0), a, v)  #move tool and keep orientation
rob.stopj(a)

rob.movel((x, y, z, rx, ry, rz), wait=False)
while True :
    time.sleep(0.1)  #sleep first since the robot may not have processed the command yet
    if rob.is_program_running():
        break

rob.movel((x, y, z, rx, ry, rz), wait=False)
while rob.getForce() < 50:
    time.sleep(0.01)
    if not rob.is_program_running():
        break
rob.stopl()

try:
    rob.movel((0,0,0.1,0,0,0), relative=True)
except (RobotError, ex):
    print("Robot could not execute move (emergency stop for example), do something", ex)

