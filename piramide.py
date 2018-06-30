from heapq import *
import numpy as np
import cv2


# conseguiu ser mais lenta para achar as distancias que a função de baixo, mesmo devendo ser melhor
# não é usada
def dijkstra(mat):
    maxd = 10000
    s = 1
    mat = mat.astype(np.int16) + maxd
    mat[mat > maxd] = 1

    vy = [1, 1, 0, -1, -1, -1, 0, 1]
    vx = [0, 1, 1, 1, 0, -1, -1, -1]
    v = np.transpose([vy, vx])

    h, w = mat.shape[:2]
    q = [(0,)+tuple(i) for i in np.argwhere(mat == 1)]
    while q:
        (cost, y, x) = heappop(q)
        if mat[y, x] <= cost:
            continue
        mat[y, x] = cost
        for i, j in v:
            next = cost + 3*(i*j == 0) + 4*(i*j != 0)
            if y+i < 0 or y+i >= h or x+j < 0 or x+j >= w or mat[y+i, x+j] <= next:
                continue
            heappush(q, (next, y+i, x+j))
    return mat


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
    return img


def scaledown(img):
    h, w = img.shape[:2]
    return img[:h-h % 2:2, :w-w % 2:2] | img[1::2, :w-w % 2:2] | img[:h-h % 2:2, 1::2] | img[1::2, 1::2]


def build(edgs, minpq):
    pir = [edgs]
    pird = [dist(edgs)]
    cv2.imwrite("piramideedgnv"+str(0)+".png", pir[-1])
    cv2.imwrite("piramidedistnv"+str(0)+".png", pird[-1])

    horw = edgs.shape[0] > edgs.shape[1]
    while pir[-1].shape[horw] > minpq:
        img = scaledown(pir[-1])
        pir.append(img)
        pird.append(dist(img))
        cv2.imwrite("piramideedgnv"+str(len(pir)-1)+".png", pir[-1])
        cv2.imwrite("piramidedistnv"+str(len(pir)-1)+".png", pird[-1]/pird[-1].max())
    return pird
