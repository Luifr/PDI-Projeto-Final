""" Extrai alguns pontos da borda do campo template
Como todas as linhas do campo seguem equações simples e medidas definidas nas regras
para extrair esses pontos bastou usar pontos igualmente espassados de suas equações"""
import numpy as np
import cv2


def showim(img):
    cv2.imshow("bag", img.astype(np.uint8))
    if cv2.waitKey(0):
        cv2.destroyAllWindows()

# distâncias em centimetros
l = 0.3
w = 150
h = 130
ah = 70
aw = 15
mcr = 20
mcpq = 24
acr = 12.5
acpqr = 12
acpq = 5
acw = 5
ach = 20
s = 5

ml = np.fromfunction(lambda i, j: i*j*5 + (1-i)*w//2, (2, h//s+1))  # midle line

# left area
laul = np.fromfunction(lambda i, j: i*30 + (1-i)*j*5, (2, aw//s+1)) # left area upper line
lall = np.fromfunction(lambda i, j: i*100 + (1-i)*j*5, (2, aw//s+1)) # left area lower line
lavl = np.fromfunction(lambda i, j: i*(30+j*5) + (1-i)*aw, (2, ah//s+1)) # left area vertical line

# right area
raul = np.fromfunction(lambda i, j: i*30 + (1-i)*(w - j*5), (2, aw//s+1)) # right area upper line
rall = np.fromfunction(lambda i, j: i*100 + (1-i)*(w - j*5), (2, aw//s+1)) # right area lower line
ravl = np.fromfunction(lambda i, j: i*(30+j*5) + (1-i)*(w - aw), (2, ah//s+1)) # right area vertical line

mc = np.fromfunction(lambda i, j: i*(h//2+mcr*np.sin(2*np.pi/mcpq*j)) + (1-i)*(w//2+mcr*np.cos(2*np.pi/mcpq*j)), (2, mcpq)) # middle circle

lac = np.fromfunction(lambda i, j: i*(h//2+acr*np.sin(np.pi/acpqr*(j-acpq//2))) + (1-i)*(acw+aw-acr+acr*np.cos(np.pi/acpqr*(j-acpq//2))), (2, acpq)) # left area circle

rac = np.fromfunction(lambda i, j: i*(h//2+acr*np.sin(np.pi/acpqr*(j+acpqr-acpq//2))) + (1-i)*(w-acw-aw+acr+acr*np.cos(np.pi/acpqr*(j+acpqr-acpq//2))), (2, acpq)) # left area circle

arr = np.hstack((ml,laul,lall,lavl,raul,rall,ravl,mc,lac,rac))

np.save("template",arr)

# f = np.zeros((h+1,w+1),np.uint8)
# f[arr[1].astype(int),arr[0].astype(int)] = 255
# showim(f)
# print(len(arr[0]))
