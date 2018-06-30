import numpy as np
import cv2


class Par:
    def __init__(self, s, r, y, x):
        self.s = s
        self.r = r
        self.y = y
        self.x = x

    def copy(self, ds, dr, dy, dx):
        return Par(self.s+ds, self.r+dr, self.y+dy, self.x+dx)
    
    def up(self):
        return Par(self.s*2, self.r, self.y*2, self.x*2)


def getscale(h, w, th, tw):
    scimg = float(h) / w
    sct = float(th) / tw
    if scimg > sct:
        return float(w)/tw
    return float(h)/th


def startpars(img, arrpts, nv):
    h, w = img.shape[:2]
    startpars = []
    scores = []
    t = np.vstack((arrpts, np.ones(arrpts.shape[1])))
    th, tw = t[1].max()-t[1].min(), t[0].max()-t[0].min()

    sc = getscale(h, w, th, tw)
    for s in np.arange(0.3*sc, sc, 1/(tw*sc)):
        for r in range(0, 180, 2**nv):
            M = cv2.getRotationMatrix2D((0, 0), r, s)
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
                    startpars.append(Par(s, r, y, x))
                    scores.append(img[rot[1].astype(int) + y, rot[0].astype(int) + x].sum())
    return startpars, scores


def judge(dist, ppts, par):
    t = np.vstack((ppts, np.ones(ppts.shape[1])))
    th, tw = t[1].max()-t[1].min(), t[0].max()-t[0].min()
    M = cv2.getRotationMatrix2D((0, 0), par.r, par.s)
    rot = M@t
    y = rot[1].astype(int)+par.y
    x = rot[0].astype(int)+par.x
    return dist[y, x].sum()


def optimize(dist, arrpts, par, nstep, nv):
    pts=[]
    scores=[]
    h, w = dist.shape[:2]
    t = np.vstack((arrpts, np.ones(arrpts.shape[1])))
    th, tw = t[1].max()-t[1].min(), t[0].max()-t[0].min()
    sc = getscale(h, w, th, tw)
    scale_step = 1/(tw*sc)
    rot_step = 2**nv
    for ds in np.arange(-nstep*scale_step, (nstep+1)*scale_step, scale_step):
        for dr in range(-nstep*rot_step, (nstep+1)*rot_step, rot_step):
            M = cv2.getRotationMatrix2D((0, 0), par.r+dr, par.s+ds)
            rot = M@t
            mai = int(rot[1].max())
            mii = int(rot[1].min())
            maj = int(rot[0].max())
            mij = int(rot[0].min())
            if maj-mij > w or mai-mii >h:
                continue
            for di in range(-min(nstep, par.y+mii),min(nstep+1, h-mai-par.y)):
                for dj in range(-min(nstep, par.x+mij),min(nstep+1, w-maj-par.x)):
                    pts.append(par.copy(ds, dr, di, dj))
                    scores.append(dist[rot[1].astype(int) + par.y+di, rot[0].astype(int) + par.x+dj].sum())
    return pts, scores
    
    
def show(img, ppts, par):
    th, tw = ppts[1].max(), ppts[0].max()
    ppts = np.vstack((ppts, np.ones(ppts.shape[1])))
    M = cv2.getRotationMatrix2D((0, 0), par.r, par.s)
    rot = M@ppts
    y = rot[1].astype(int)+par.y
    x = rot[0].astype(int)+par.x
    img[y, x] = (0, 0, 255)
    img[par.y,par.x] = (0,255,0)
    cv2.imshow("bag", img)
    if cv2.waitKey(0):
        cv2.destroyAllWindows()
    
    
def save(img, ppts, par, name):
    th, tw = ppts[1].max(), ppts[0].max()
    ppts = np.vstack((ppts, np.ones(ppts.shape[1])))
    M = cv2.getRotationMatrix2D((0, 0), par.r, par.s)
    rot = M@ppts
    y = rot[1].astype(int)+par.y
    x = rot[0].astype(int)+par.x
    img[y, x] = (0, 0, 255)
    img[par.y,par.x] = (0,255,0)
    cv2.imwrite(name+".png",img)

