import numpy as np
import cv2

h = 1300
w = 1500
ah = 700
aw = 150
cr = 200
car = 125
caw = 50
cah = 200

f = np.zeros((h, w), dtype=np.uint8)
f[:, w//2 - 1:w//2 + 1] = 255  # midle line

# left area
f[h//2 - ah//2 - 1:h//2 - ah//2 + 1, :aw] = 255
f[h//2 + ah//2 - 1:h//2 + ah//2 + 1, :aw] = 255
f[h//2 - ah//2:h//2 + ah//2, aw - 1:aw + 1] = 255

# right area
f[h//2 - ah//2 - 1:h//2 - ah//2 + 1, w - aw:] = 255
f[h//2 + ah//2 - 1:h//2 + ah//2 + 1, w - aw:] = 255
f[h//2 - ah//2:h//2 + ah//2, w - aw - 1: w - aw + 1] = 255

# central circle
cv2.circle(f, (w//2, h//2), cr, 255, 2)

# area circle template
circle = np.zeros((car*2+6, car*2+6), dtype=np.uint8)
cv2.circle(circle, (car+3, car+3), car, 255, 2)

#left area circle
f[h//2 - cah//2 - 3: h//2 + cah//2 + 3, aw + 1: aw + caw + 3] = circle[car + 3 - cah//2 - 3:car + 3 + cah//2 + 3, - caw-2 :]

#right area circle
f[h//2 - cah//2 - 3: h//2 + cah//2 + 3, w - aw - caw - 3: w - aw -1] = circle[car + 3 - cah//2 - 3:car + 3 + cah//2 + 3, :caw + 2]


def showim(img):
    cv2.imshow("bag", img)
    if cv2.waitKey(0):
        cv2.destroyAllWindows()

cv2.imwrite("template.png",f)
showim(f)
