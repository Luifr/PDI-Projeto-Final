import numpy as np
import cv2


def scaledown(img):
    h, w = img.shape[:2]
    return img[:h-h % 2:2, :w-w % 2:2] | img[1::2, :w-w % 2:2] | img[:h-h % 2:2, 1::2] | img[1::2, 1::2]


def dist(img):
    maxd = 10000
    s = 1
    img = img.astype(np.int16) + maxd
    img[img > maxd] = 0

    while img.max() == maxd:
        img[:, s:] = np.minimum(img[:, :-s]+3, img[:, s:])  # l
        img[:, :-s] = np.minimum(img[:, s:]+3, img[:, :-s])  # r
        img[s:, :] = np.minimum(img[:-s, :]+3, img[s:, :])  # u
        img[:-s, :] = np.minimum(img[s:, :]+3, img[:-s, :])  # d

        img[s:, s:] = np.minimum(img[:-s, :-s]+4, img[s:, s:])  # lu
        img[:-s, :-s] = np.minimum(img[s:, s:]+4, img[:-s, :-s])  # rd
        img[s:, :-s] = np.minimum(img[:-s, s:]+4, img[s:, :-s])  # ru
        img[:-s, s:] = np.minimum(img[s:, :-s]+4, img[:-s, s:])  # ld
    print(img.max())
    return img


pir = [cv2.imread("edge.png", cv2.IMREAD_GRAYSCALE)]
pird = [dist(pir[0])]

while pir[-1].shape[0] > 50:
    img = scaledown(pir[-1])
    pir.append(img)
    pird.append(dist(img))
    print(pir[-1].shape)
    np.save("dist"+str(len(pir)-1), pird[-1])
