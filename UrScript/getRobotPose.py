import urx
import sys

a = 0.3
v = 0.5
robot = urx.Robot("192.168.0.16")
# pose_j = [3.2224669456481934, -1.6972586117186488, 1.4982417265521448, -1.3831556600383301, -1.5768340269671839,
#           1.65024995803833]
# robot.movej(pose_j, a, v, wait=True)

if input("Get data?")=="y":
    joint_angles = robot.getj()
    joint_pos = robot.getl()
    print("Robot joint position is ", joint_angles)
    print("Robot ll position is ", joint_pos)

else:
    sys.close()

