#Trabalho final PDI
Projeto Final - PDI

IDENTIFICAR O CAMPO -- tudo feito menos remover o efeito barrel
- Remover o efeito barrel da camera -- não feito
- Criar um template do campo para pegar as features relevantes(para comparar com os obtidos da imagem teste) -- completo
- Encontrar e relacionar essas features de forma a mapear esses pontos para os pontos no template (atualmente edges)
-> algorimo sendo testado é Hierarchical chamfer matching: https://people.eecs.berkeley.edu/~malik/cs294/borgefors88.pdf
    1) Extrair as bordas -- completo
    2) Construir a piramide de distancias -- completo
    3) Escolher os pontos de borda do template para serem usados no poligono --completo
    4) encontrar no topo da piramide (distancias com a pior resolução) possiveis posições para o campo --completo
    5) ir descendo na piramide com cada posição afinando suas medidas (devido ao aumento da resolução) e escolher a melhor -- completo

IDENTIFICAR A BOLINHA -- não feito
- Segmentar o unico objeto laranja dentro do campo
- Usar a função de mapeamento do campo sem paralax para descobrir a posição da bolinha no campo

INDENTIFICAR OS ROBOS -- não feito
- Identificar a posição do robo na imagem obtida pela camera
- Usar a função de mapeamento do campo modificada para mapear uma posição 7,5 cm a cima no campo template (altura do robo)
