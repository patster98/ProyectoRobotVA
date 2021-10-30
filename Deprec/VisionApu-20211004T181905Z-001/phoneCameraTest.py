import cv2
import time

if __name__ == '__main__':
    cap = cv2.VideoCapture(1)  #abro el canal de la webcam del sist = 0
    time.sleep(60)
    print("starting loop")
    while True:
        success, image = cap.read() #agrego el _ porq no me importa ese param
        count = 0
        cv2.imshow("Webcam", image)
        while success:
            if cv2.waitKey(1) & 0xFF == ord('c'):
                cv2.imwrite("frame%d.jpg" % count, image)  # save frame as JPEG file
                success, image = cap.read()
                print('Read a new frame: ', success)
                count += 1

        if cv2.waitKey(1) & 0xFF == ord('z'): #si apreto z (chequea el codigo ascii) me apaga el programa
            break
