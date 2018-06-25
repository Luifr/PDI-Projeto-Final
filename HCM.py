import numpy as np
import cv2


class Par:
    def __init__(self, s, r, y, x):
        self.s = s
        self.r = r
        self.y = y
        self.x = x


def startpts(h, w, arrpts):
    startpts = []
    t = np.vstack((arrpts, np.ones(arrpts.shape[1])))
    th, tw = t[1].max(), t[0].max()

    scimg = float(h) / w
    sct = float(th) / tw
    if scimg > sct:
        sc = float(w)/tw
    else:
        sc = float(h)/th

    for s in np.arange(0.3*sc, sc, 0.1*sc):
        for r in range(0, 180, 15):
            M = cv2.getRotationMatrix2D((th/2, tw/2), r, s)
            rot = M@t
            mai = int(rot[1].max())
            mii = int(rot[1].min())
            maj = int(rot[0].max())
            mij = int(rot[0].min())
            if maj-mij > w:
                continue
            for di in range(h-mai+mii):
                for dj in range(w-maj+mij):
                    y = di-mii
                    x = dj-mij
                    startpts.append(Par(s, r, y, x))
    return startpts


def judge(dist, ppts, par):
    th, tw = ppts[1].max(), ppts[0].max()
    ppts = np.vstack((ppts, np.ones(ppts.shape[1])))
    M = cv2.getRotationMatrix2D((th/2, tw/2), par.r, par.s)
    rot = M@ppts
    y = rot[1].astype(int)+par.y
    x = rot[0].astype(int)+par.x
    return dist[y, x].sum()


def show(img, ppts, par):
    th, tw = ppts[1].max(), ppts[0].max()
    ppts = np.vstack((ppts, np.ones(ppts.shape[1])))
    M = cv2.getRotationMatrix2D((th/2, tw/2), par.r, par.s)
    rot = M@ppts
    y = rot[1].astype(int)+par.y
    x = rot[0].astype(int)+par.x
    img[y, x] = (0, 0, 255)
    cv2.imshow("bag", img)
    if cv2.waitKey(0):
        cv2.destroyAllWindows()
