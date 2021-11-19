import urx
import sys

robot =  urx.Robot("192.168.0.16")
if input("Get data?")=="y":
    joint_angles = robot.getj()
    print("Robot joint position is ", joint_angles)
else:
    sys.

