import time
from math import pi
import numpy as np
import urx

from Regression import regresion_x as rx, regresion_y as ry
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper

rob = urx.Robot("192.168.0.16")
gripper = Robotiq_Two_Finger_Gripper(rob)


def robot(x, y, angle, contador):

    contador +=1



    try:
        # Get current robot joint angles in radians
        init_joint_angles = rob.getj()
        print("Initial joint position is ", init_joint_angles)

        # pose_1 = [3.2759432792663574, -1.2038753789714356, 1.8174002806292933, -2.2467409572997035, -1.5875690619098108,
        #           2.2951483726501465]
        pose_1 = [1.7542033195495605, -1.9955908260741175, 2.6349318663226526, -2.1839128933348597, -1.5938661734210413,
         0.8319950103759766]
        # Move robot to new position
        pose_in = [3.1093735694885254, -1.6083599529662074, 1.417511288319723, -1.3918422025493165, -1.575754467641012,
                   1.5372142791748047]

        a = 0.3
        v = 0.7

        print("Moving to ", pose_in)
        rob.movej(pose_in, a, v, wait=True)

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
        subir=[0, 0, 0.3, 0, 0, 0]


        print("Moving to ", pose_gripper)
        rob.movel(pose_gripper, a, v, wait=True, relative=True)

        print("Closing")
        gripper.close_gripper()

        print("Moving to ", pose_gripper)
        rob.movel(subir, a, v, wait=True, relative=True)

        print("Moving to ", pose_1)
        rob.movej(pose_1, a, v, wait=True)

        print("Dejando pieza")
        gripper.open_gripper()

        print("Moving to ", pose_gripper)
        rob.movel(subir, a, v, wait=True, relative=True)




    finally:
        # # Close robot connection
        # print("Closing robot connection")
        # rob.close()
        finish = True


    return contador,finish