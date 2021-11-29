import time
from math import pi
import numpy as np
import urx

from Regression import regresion_x as rx, regresion_y as ry
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
rob = urx.Robot("192.168.0.16")
gripper = Robotiq_Two_Finger_Gripper(rob)


pose_in = [3.1093735694885254, -1.6083599529662074, 1.417511288319723, -1.3918422025493165, -1.575754467641012,
                   1.5372142791748047]

a = 0.3
v = 0.5

# rob.movej(pose_in, a, v, wait=True)
move = rob.getl()
print(move)

def robot(x, y, angle, contador):

    rob = urx.Robot("192.168.0.16")
    gripper = Robotiq_Two_Finger_Gripper(rob)


    try:
        # Get current robot joint angles in radians
        init_joint_angles = rob.getj()
        print("Initial joint position is ", init_joint_angles)


        pose_l = [0.4166700510736631+(contador/100), 0.17632951082862758, 0.3693618977251729, 0.0013343769722733135, 3.127955852012821, -0.0065696793773294465]

        # Move robot to new position
        pose_j = [3.2224669456481934, -1.6972586117186488, 1.4982417265521448, -1.3831556600383301, -1.5768340269671839, 1.65024995803833]

        a = 0.3
        v = 0.5

        print("Moving to ", pose_j)
        rob.movej(pose_j, a, v, wait=True)

        # Cambie el is_running por el is_program_running en el wait for move

        move = rob.getl()
        move[0] = x - 0.01
        move[1] = y - 0.06
        print("Moving to ", move)
        rob.movel(move, a, v, wait=True, relative=False)

        t = rob.get_pose()

        z = -move[2] + 0.02

        t.orient.rotate_z(angle*pi/180)
        rob.set_pose(t, a, v)

        pose_gripper = [0, 0, z, 0, 0, 0]
        subir=[0, 0, 0.4, 0, 0, 0]


        print("Moving to ", pose_gripper)
        rob.movel(pose_gripper, a, v, wait=True, relative=True)

        print("Closing")
        gripper.close_gripper()

        print("Subiendo ")
        rob.movel(subir, a, v, wait=True, relative=True)

        print("Moving to ", pose_l)
        rob.movel(pose_l, a, v, wait=True)

        print("Bajando")
        rob.movel(pose_gripper, a, v, wait=True, relative=True)

        print("Dejando pieza")
        gripper.open_gripper()

        print("Moving to ", pose_gripper)
        rob.movel(subir, a, v, wait=True, relative=True)

    finally:
        # Close robot connection
        print("Closing robot connection")
        rob.close()

    contador += 1

    return contador