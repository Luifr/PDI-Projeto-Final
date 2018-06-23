import sys
import numpy as np
import cv2

if sys.argv[1] == None:
    print("nenhuma imagem pra ler")
    exit()

img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
edg = cv2.Canny(img, 70, 255)
cv2.imwrite("edge.png",edg)

def showim(img):
    cv2.imshow("bag", img.astype(np.uint8))
    if cv2.waitKey(0):
        cv2.destroyAllWindows()
