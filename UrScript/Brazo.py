import urx
import time
from numpy import pi
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper

# Create robot instance
rob = urx.Robot("192.168.0.16")
# Create gripper instance
gripper = Robotiq_Two_Finger_Gripper(rob)

# Use try-finally to ensure robot is closed on exit
try:
    # Close gripper
    print("Closing")
    gripper.close_gripper()

    # Open gripper
    print("Opening")
    gripper.open_gripper()

    t = rob.get_pose()

    t.orient.rotate_z(pi/6)
    rob.set_pose(t, vel=0.3, acc=0.3)

finally:
    # Close robot connection
    print("Closing robot connection")
    rob.close()