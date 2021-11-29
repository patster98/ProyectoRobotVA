import math
import numpy as np
import cv2
def draw_lines(img, origin, x_axis, y_axis, x_text, y_text):
  line_thickness = 4
  cv2.arrowedLine(img, origin, y_axis, (0, 255, 0), thickness=line_thickness)
  cv2.arrowedLine(img, origin, x_axis, (0, 255, 0), thickness=line_thickness)
  cv2.putText(img, "x", x_text,
              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
  cv2.putText(img, "y", y_text,
              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

def to_tuple(arr):
  return (arr[0], arr[1])

def inverse_contour_points(shape_contour):
  new_contours = map(invert_point, shape_contour)
  new_contours = np.array(list(new_contours))
  return new_contours

def invert_point(x):
  x = np.array(x, dtype='float32')
  original_points = cv2.perspectiveTransform(x[np.newaxis], inverse_mat)
  result = list(map(lambda x: np.array([math.floor(x[0]), math.floor(x[1])]),original_points[0]))
  result = np.array(result)
  return result

def draw_circle_with_text(img, x, y, label,grad):
  cv2.circle(img, (x, y), 7, (255, 255, 255), -1)
  cv2.putText(img,"C: "+ label, (x - 20, y - 40),
              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
  cv2.putText(img, grad, (x + 20, y - 20),
              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
  cv2.putText(img,"C: "+ "(" + str(x) + " px" ", " + str(y) + " px" ")", (x - 20, y - 60),
              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

def obtain_contour(img):
  gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
  block_size = 67  # Tamaño del bloque a comparar, debe ser impar.
  bin = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, 2)

  # Invert the image so the area of the UAV is filled with 1's. This is necessary since
  # cv::findContours describes the boundary of areas consisting of 1's.
  bin = 255 - bin  # como sabemos que las figuras son negras invertimos los valores binarios para que esten en 1.

  kernel = np.ones((3, 3), np.uint8)  # Tamaño del bloque a recorrer
  # buscamos eliminar falsos positivos (puntos blancos en el fondo) para eliminar ruido.
  bin = cv2.morphologyEx(bin, cv2.MORPH_ERODE, kernel)

  contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST,
                                         cv2.CHAIN_APPROX_SIMPLE)  # encuetra los contornos, chain aprox simple une algunos puntos para que no sea discontinuo.
  return max(contours, key=cv2.contourArea)  # Agarra el contorno de area maxima

def draw_axis(frame, perpendicular_img):
  draw_lines(perpendicular_img, (0,0),(width, 0), (0, height), (width - 50, 20), (20, height - 50))
  inverted_origin = invert_point([[0, 0]])[0]
  y_axis = invert_point([[0, height]])[0]
  x_axis = invert_point([[width, 0]])[0]
  y_text = invert_point([[20, height + 50]])[0]
  x_text = invert_point([[width + 50, 20]])[0]
  draw_lines(frame, to_tuple(inverted_origin),to_tuple(x_axis), to_tuple(y_axis), to_tuple(x_text), to_tuple(y_text))

def NormalizeVector(v):
    normVec = [v[0]/v[2],v[1]/v[2],v[2]/v[2]]
    return normVec

from mainRobot import robot
from h_matrix import obtain_h_matrix, robot_matrix
from undistort import camara_undistort


width, height = 500, 500
width_cm, height_cm = 39.5,37.5

cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)

contador = 0
finish=True
M1 = 0
global h_mat
global inverse_h_mat
h_mat = []
inverse_h_mat = []
img_counter = 0

while True:

    ret, raw = cap.read()
    frame = camara_undistort(raw)

    if cv2.waitKey(1) == ord('c'):
        h_mat = obtain_h_matrix(frame)
        inverse_mat = cv2.invert(h_mat)[1]
        matrizRob = robot_matrix(frame)
        print("matriz rob", matrizRob)


    if(len(h_mat) != 0):
        perpendicular_img = cv2.warpPerspective(frame, h_mat, ((width, height)))

        shape_contour = obtain_contour(perpendicular_img)
        if(cv2.contourArea(shape_contour) > 5000):
            MaxCont = shape_contour
            cv2.drawContours(perpendicular_img, [shape_contour], -1, (255, 0, 255), 3)

            M2 = cv2.moments(shape_contour)

            cX = int(M2["m10"] / M2["m00"])
            cY = int(M2["m01"] / M2["m00"])
            # time.sleep(1)


            if cv2.waitKey(1) & 0xFF == ord(" "):
                # coord homog del centro de pieza en las coord de la img warpeada
                warpPoint = np.append([cX,cY], [1])
                coordHomog = np.dot(matrizRob, warpPoint)
                coordRobot = NormalizeVector(coordHomog)
                print("Vector homografía: ", coordHomog)
                print("Vector robot: ", coordRobot)
            # coord homog del centro de pieza en las coord de la img warpeada
            warpPoint = np.append([cX, cY], [1])
            coordHomog = np.dot(matrizRob, warpPoint)
            coordRobot = NormalizeVector(coordHomog)

            x_mm = np.round(coordRobot[0],5)*1000
            y_mm = np.round(coordRobot[1],5)*1000

            original_contours = inverse_contour_points(shape_contour)
            cv2.drawContours(frame, [original_contours], -1, (255, 0, 255), 3)
            approx = cv2.approxPolyDP(shape_contour, 0.001*cv2.arcLength(shape_contour, True), True)
            perimeter = cv2.arcLength(shape_contour,True)
            approx = cv2.approxPolyDP(shape_contour, 0.04 * perimeter, True)
            _ ,_ ,angle = cv2.fitEllipse(shape_contour)
            angle=round(angle)
            P1x = cX
            P1y = cY
            length = 35

            if M2["m00"]==M1 and finish:
                finish=False
                contador,finish = robot(coordRobot[0], coordRobot[1],angle,contador)
                print("angle: ", angle)

            else:
                M1 = M2["m00"]
                print("Momento: ", M2["m00"])

            #calculate vector line at angle of bounding box
            P2x = int(P1x + length * np.cos(np.radians(angle)))
            P2y = int(P1y + length * np.sin(np.radians(angle)))
            #draw vector line
            cv2.line(perpendicular_img,(cX, cY),(P2x,P2y),(255,255,255),5)

            inverted_point = invert_point([[cX, cY]])[0]
            draw_circle_with_text(perpendicular_img, cX, cY, "(" + str(x_mm) + " mm" ", " + str(y_mm) + " mm" ")", str(angle) + "gr")
            draw_circle_with_text(frame, inverted_point[0], inverted_point[1], "(" + str(x_mm) + ", " + str(y_mm) + ") mm", "")

        draw_axis(frame, perpendicular_img)
        cv2.imshow("Homography ", perpendicular_img)

    cv2.imshow("Live Image ", frame)
    if cv2.waitKey(1) & 0xFF == ord('q') or contador==4:
        # Close robot connection
        print("Closing robot connection")
        break
cv2.destroyAllWindows()
raise SystemExit
