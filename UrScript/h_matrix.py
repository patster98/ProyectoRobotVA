import cv2
import numpy as np
x1 = 0.35001
y1 = 0.050
x2 = 0.75002
y2 = 0.050
x4 = 0.750002
y4 = -0.325
x3 = 0.35001
y3 = -0.325
width, height = 500, 500
counter = 0
coordRob = np.zeros((4, 2), np.int)

def obtain_h_matrix(img):
  global circles
  # declaro array vacio donde voy a guardar los puntos
  circles = np.zeros((4, 2), np.int)

  def mousePoints(event, x, y, flags, params):
    global counter
    if event == cv2.EVENT_LBUTTONDOWN:
      circles[counter] = x, y
      counter = counter + 1

  while True:
    if counter == 4:
      origin = np.float32([circles[0], circles[1], circles[2], circles[3]])
      target = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
      matrix = cv2.getPerspectiveTransform(origin, target)
      cv2.destroyWindow("Calibration Image ")
      return matrix

    for x in range(0, counter):
      cv2.circle(img, (circles[x][0], circles[x][1]), 3, (0, 255, 0), cv2.FILLED)

    cv2.imshow("Calibration Image ", img)
    cv2.setMouseCallback("Calibration Image ", mousePoints)
    cv2.waitKey(1)

def robot_matrix(screen):
  # Estos puntos están en la img original, hay que pasarlo a la warped
  # origin = np.float32([circles[0], circles[1], circles[2], circles[3]])
  origin = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
  coordRb = np.float32([[x1,y1],[x2,y2], [x3,y3], [x4,y4]])
  robMatrix = cv2.getPerspectiveTransform(origin, coordRb)
  cv2.circle(screen,(circles[1][0], circles[1][1]), 3, (255, 255, 0), cv2.FILLED)
  return robMatrix
