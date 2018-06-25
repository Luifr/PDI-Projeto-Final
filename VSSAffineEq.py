import sys
import numpy as np
import cv2
import piramide
import fazpoligono
import HCM

if len(sys.argv) < 2:
    print("nenhuma imagem pra ler")
    exit()

img = cv2.imread(sys.argv[1])
h, w = img.shape[:2]
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edg = cv2.Canny(gray, 70, 255)
pirdist = piramide.build(edg, 100)
polygpts = fazpoligono.campoVSS()

#teste no topo da piramide
hp, wp = pirdist[-1].shape[:2]
startpts = HCM.startpts(hp, wp, polygpts)
scores = [HCM.judge(pirdist[-1], polygpts, i) for i in startpts]
m = np.argmin(scores)
floor = img
for i in range(len(pirdist)-1):
    floor = cv2.pyrDown(floor)
print("escala:",startpts[m].s," rotação:",startpts[m].r," x:",startpts[m].x," y:",startpts[m].y,)
HCM.show(floor, polygpts, startpts[m])