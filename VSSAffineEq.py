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

#piramide de distancia até a borda mais próxima
distpir = piramide.build(edg, 100)

#piramide da imagem de entrada, para vizualizar os pontos em cada nivel (mais a frente)
imgpir = [img]
for i in range(len(distpir)-1):
    imgpir.append(cv2.pyrDown(imgpir[-1]))

#pontos de borda do campo
polygpts = fazpoligono.campoVSS()

# vizualização dos pontos de borda do campo
f = np.zeros((131, 151), np.uint8)
f[polygpts[1].astype(int) + 65, polygpts[0].astype(int) + 75] = 255
cv2.imwrite("pontosdotemplate.png", f)

# descobre os parametros de translação, escala e rotação do campo capturado pela câmera
# faz diferente do proposto, pega apenas o melhor de cada nível e usa no próximo
pars, scores = HCM.startpars(distpir[-1], polygpts, len(distpir)-1) # testa todas asa variações de parametros no 1 nivel
for i in range(2, len(distpir)+1): # passa pelo segundo nivel da piramide até sua base otimizando o melhor parametro achado no topo
    m = np.argmin(scores)
    HCM.save(imgpir[-i+1], polygpts, pars[m],"resultnv"+str(-i+1)) # salva o resultado do nivel anterior
    sel = pars[m].up() # seleciona o melhor do nível passado e adequa seus parametros ao nivel acima
    pars, scores = HCM.optimize(distpir[-i], polygpts, sel, 10, len(distpir)-i) # testa variações do melhor parametro do nivel de cima

m = np.argmin(scores)
par = pars[m] # completou o objetivo do programa, achar os parametros do campo na imagem para depois extrair as posições dos robos
print("escala:", par.s, " rotação:", par.r, " x:", par.x, " y:", par.y, "erro: ", scores[m]) # exibe o resultado
HCM.show(imgpir[0], polygpts, par) # exibe a imagem para visualizar onde o programa achou os melhores pontos do campo
cv2.imwrite("resultnv"+str(len(distpir))+".png",imgpir[0]) # salva ela também

# recorta o campo da imagem para reconhecer os robos, é para ser feito em tempo real
M = cv2.getRotationMatrix2D((par.x, par.y), par.r, 1)
Minv = cv2.invertAffineTransform(M)
res = cv2.warpAffine(img, Minv, (w,h))
M = cv2.getRotationMatrix2D((0, 0), 0, 1)
M[0, 2] -= par.x - 75*par.s
M[1, 2] -= par.y - 65*par.s
res = cv2.warpAffine(res, M, (int(150*par.s), int(130*par.s)))
cv2.imshow("RESULTADO", res)
if cv2.waitKey(0):
    cv2.destroyAllWindows()
cv2.imwrite("RESULTADO.png",res)
