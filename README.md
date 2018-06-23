#Trabalho final PDI
Projeto Final - PDI

IDENTIFICAR O CAMPO
- Remover o efeito barrel da camera
- Criar um template do campo para pegar as features relevantes(para comparar com os obtidos da imagem teste) -- completo
- Encontrar e relacionar essas features de forma a mapear esses pontos para os pontos no template (atualmente edges)
    -> algorimo sendo testado https://people.eecs.berkeley.edu/~malik/cs294/borgefors88.pdf

IDENTIFICAR A BOLINHA
- Segmentar o unico objeto laranja dentro do campo
- Usar a função de mapeamento do campo sem paralax para descobrir a posição da bolinha no campo template

INDENTIFICAR OS ROBOS
- Identificar a direçao e a posição do robo na imagem obtida pela camera
- Usar a função de mapeamento do campo modificada para mapear uma posição 7,5 cm a cima no campo template (altura do robo)
