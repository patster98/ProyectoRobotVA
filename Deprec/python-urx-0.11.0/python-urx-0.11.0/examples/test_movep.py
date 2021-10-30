import time 
import urx
import logging


if __name__ == "__main__":
    rob = urx.Robot("192.168.0.16")
    try:
        l = 0.1
        v = 0.3
        a = 0.3
        r = 0.05
        pose = rob.getl()
        pose[2] += l
        rob.movep(pose, acc=a, vel=v, wait=True)
        while True:
            p = rob.getl(wait=True)
            if p[2] > pose[2] - 0.05:
                break

        pose[1] += l 
        rob.movep(pose, acc=a, vel=v, wait=True)
        while True:
            p = rob.getl(wait=True)
            if p[1] > pose[1] - 0.05:
                break

        pose[2] -= l
        rob.movep(pose, acc=a, vel=v, wait=True)
        while True:
            p = rob.getl(wait=True)
            if p[2] < pose[2] + 0.05:
                break

        pose[1] -= l
        rob.movep(pose, acc=a, vel=v, wait=True)

    finally:
        rob.close()

