from operator import itemgetter, attrgetter

class coordenada:
    x=-1
    y=-1
    dominado=False
    nroDominado=0

    def __init__(self, x, y):
        self.x=x
        self.y=y




class cpareto:
    coordenadas=[]

    def __init__(self, coordenadas):
        for coor in coordenadas:
            self.coordenadas.append(coordenada(coor[0], coor[1]))



    def ordenar(self, criterio):
        #atributo por el cual ordenar
        if criterio==1:
            self.coordenadas= sorted(self.coordenadas, key=lambda coordenada: coordenada.x)
        elif criterio == 2:
            self.coordenadas= sorted(self.coordenadas, key=lambda coordenada: coordenada.y)
        else:
            self.coordenadas= sorted(self.coordenadas, key=lambda coordenada: coordenada.nroDominado)



    def obtenerFrentePareto(self):
        print(len(self.coordenadas))
        for i in range(0, len(self.coordenadas)):
            for j in range (0, i-1):
                if self.coordenadas[i].x > self.coordenadas[j].x and self.coordenadas[i].y > self.coordenadas[j].y:
                    #print("entro pio")
                    self.coordenadas[i].dominado=True
                    
                    if self.coordenadas[j].dominado==False:
                        self.coordenadas[i].nroDominado+=1
            
            
                
                 

        

    def imprimir(self):
        for coor in self.coordenadas:
            print ("[",coor.x," ; ",coor.y,"] \tdominado: ",coor.dominado," \tnroDominado: ",coor.nroDominado)







def main():
    conjuntoPareto=cpareto([
        [2,3],
        [4,4],
        [3,12],
        [3,8],
        [5,2],
        [2,6],
        [5,11],
        [6,10],
        [7,7],
        [8,1],
        [8,2],
        [8,3],
        [8,5],
        [11,5],
        [12,2],
        [14,3]
    ])


    conjuntoPareto.ordenar(1)
    conjuntoPareto.obtenerFrentePareto()
    conjuntoPareto.imprimir()




main()