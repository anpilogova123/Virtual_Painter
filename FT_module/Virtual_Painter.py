import fingertrackingmodule as ftm 
import cv2
import os
import numpy as np 

HEADER_LIST = []
BRUSH_THICKNESS = 25
ERASE_THICKNESS = 100
DRAW = False 
DRAW_COLOR = (0, 0, 0)
FOLDER_HEADERS = "Header"

imgCanvas = np.zeros((1080, 1920), np.uint8) 

myList = os.listdir(FOLDER_HEADERS)
for imgPath in myList:
    image = cv2.imread(FOLDER_HEADERS+'/'+imgPath)
    HEADER_LIST.append(image)
header = HEADER_LIST[-1]


WIDHT = 1920
HEIGHT = 1080

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDHT)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

detector = ftm.handDetector()

while cap.isOpened():  # пока камера "работает"
    success, image = cap.read()  # получение кадра с камеры
    if not success:  # если не удалось получить кадр
        print('Не удалось получить кадр с web-камеры')
        continue  # возвращаемся к ближайшему циклу
    image = cv2.flip(image, 1)  # зеркально отражаем изображение
    detector.findHands(image)
    detector.findFingersPosition(image)
    h, w, c = header.shape
    if detector.result.multi_hand_landmarks: # нашлись ли руки 
            handCount = len(detector.result.multi_hand_landmarks) # кол-во
            for i in range(handCount):
                x1, y1 = detector.pointPosition[i][4][0], detector.pointPosition[i][4][1]
                x2, y2 = detector.pointPosition[i][8][0], detector.pointPosition[i][8][1]
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                 
                distance = detector.findDistance(4, 8, i)
                cv2.putText(image, f"{cx} {cy} {distance}", (200, 600), cv2.FONT_ITALIC, 2, (255, 255, 255), 2)
                if distance < 45:
                    if cy < h:
                        if 720 <= cx <= 900:
                            header = HEADER_LIST[1]
                            DRAW_COlOR = []
                        elif 1056 <= cx <= 1250:
                            header = HEADER_LIST[2]
                        elif 1420 <= 1620:
                            header = HEADER_LIST[3]
                        elif 1700 <=  cx <= 1870:
                            header = HEADER_LIST[4]





    
    dim = (1920, h)
  
    # resize image
    header = cv2.resize(header, dim, interpolation = cv2.INTER_AREA)
    w = 1920
    image[0:h, 0:w] = header 
    cv2.imshow('window', image)
    if cv2.waitKey(1) & 0xFF == 27:  # Ожидаем нажатие ESC 
            break

