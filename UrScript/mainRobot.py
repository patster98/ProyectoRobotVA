import time
from math import pi
import numpy as np
import urx

from Regression import regresion_x as rx,regresion_y as ry
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper

def robot(x,y,angle):


    #
    # from mainapu import MainVA as va
    #
    #
    # x= rx(0.3088)
    # y= ry(0.0754)
    # Rad=pi/3
    # va(0)

    # print('predicted response:', x,y, sep='\n')
    # Create robot instance


    rob = urx.Robot("192.168.0.16")
    gripper = Robotiq_Two_Finger_Gripper(rob)

    # Use try-finally to ensure robot is closed on exit
    try:
        # Get current robot joint angles in radians
        init_joint_angles = rob.getj()
        print("Initial joint position is ", init_joint_angles)
        pose_1 = [2, -1.6088158092894496, 1.4181464354144495, -1.391148881321289, -1.5592621008502405, 1.0196056365966797]

        # Move robot to new position
        pose_in = [3.1093735694885254, -1.6083599529662074, 1.417511288319723, -1.3918422025493165, -1.575754467641012, 1.5372142791748047]

        a=0.3
        v=0.5



        print("Moving to ", pose_in)
        rob.movej(pose_in, a, v ,wait=True)

         # Cambie el is_running por el is_program_running en el wait for move

        move= rob.getl()
        move[0] = x
        move[1] = y
        print("Moving to ", move)
        rob.movel(move, a, v, wait=True,relative=False)




        t = rob.get_pose()

        z = -move[2] - 0.02


        t.orient.rotate_z(angle)
        rob.set_pose(t,a,v)

        pose_gripper = [0, 0, z, 0, 0, 0]

        print("Moving to ", pose_gripper)
        rob.movel(pose_gripper, a, v, wait=True, relative=True)

        print("Closing")
        gripper.close_gripper()

        print("Moving to ", pose_1)
        rob.movej(pose_1, a, v, wait=True)



    finally:
        # Close robot connection
        print("Closing robot connection")
        rob.close()





robot(0.2,-0.3,60)
