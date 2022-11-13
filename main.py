import random

class Ciudad:
    # Una ciudad puede tener costo y tiempo
    # Existe el caso de costo 0, pero no de tiempo 0
    def __init__(self, costo, tiempo):
        self.costo = costo
        self.tiempo = tiempo
    
    # Se imprime de la forma [costo,tiempo]
    def imprimirCiudad(self):
        print("[",self.costo,",",self.tiempo,"]",end="")

    def getCosto(self):
        return self.costo
    
    def getTiempo(self):
        return self.tiempo

        

# Los genes de los cromosomas sera el orden en que el viajero va a recorrer las ciudades
# Se debe tener una estructura que defina el costo y el tiempo entre ciudades
# El pareto es [costo total y tiempo total]
# El fitness se calcula como un spea
# Se evoluciona por mutacion

# Datos sobre las ciudades
nroCiudades = 0
maxCosto = 0
maxTiempo = 0
ciudades = []

# Datos sobre la poblacion
tamanhoPoblacion = 0
# gen = {Costo, tiempo}
poblacion = []
# pareto {CostoTotal, tiempoTotal}
paretoSet = []
frentePareto = []

# Datos varios
# Cantidad de iteraciones(maximo)
iteraciones = 0

'''
    si nroCiudades = 3

    ciudades[nroCiudades][nroCiudades] = { 
                    { [1,3], [4,2], [3,0]},
                    { [5,2], [1,3], [8,2] },
                    { [2,1], [3,5], [9,2] }
                    };

'''

def parametros():
    global nroCiudades,maxCosto,maxTiempo,tamanhoPoblacion
    
    print ("Introduce el numero de ciudades:")
    nroCiudades = int(input()) + 1
    print ("Introduce costo maxima entre ciudades:")
    maxCosto = int(input())
    print ("Introduce tiempoo maximo entre ciudades:")
    maxTiempo = int(input())
    print ("Introduce el tamaño de la poblacion:")
    tamanhoPoblacion = int(input())
    print ("Introduce la cantidad de iteraciones:")
    iteraciones = int(input())

def generarCiudades():
    global nroCiudades,ciudades,maxCosto,maxTiempo
    # tenemos en cuenta un grafo completo
    for i in range(0,nroCiudades):
        # Datos de las ciudades a los que se puede llegar a a partir de la ciudad i
        ciudad = []

        # Se calcula datos aleatorios de las ciudades(j) a los que se puede llegar a a partir de la ciudad i
        for j in range(0,nroCiudades):
            if i != j:
                ciudad.append( Ciudad(random.randint(0, maxCosto),random.randint(1, maxTiempo))  )
            else:
                ciudad.append( Ciudad(0,0) )
        ciudades.append(ciudad)

def generarPoblacionInicial():
    global tamanhoPoblacion, nroCiudades, poblacion
    for i in range(0,tamanhoPoblacion):
        listaCiudades = list(range(0,nroCiudades-1))
        cromosoma = [0] 
        while(listaCiudades !=[]):
            gen = random.choice(listaCiudades)
            cromosoma.append(gen+1)
            listaCiudades.remove(gen)
        cromosoma.append(0)
        poblacion.append(cromosoma)

def calcularPareto():
    global paretoSet, poblacion, ciudades, tamanhoPoblacion 
    for cromosoma in poblacion:

        costoTotal = 0
        tiempoTotal = 0
        
        for i in range(0,len(cromosoma) - 1):

            gen = cromosoma[i]

            ciudadOrigen = gen
            ciudadDestino = cromosoma[gen + 1]

            # obtenemos la distancia de la ciudad origen a la ciudad destino
            distancias = ciudades[ciudadOrigen]
            distancias[ciudadDestino].getCosto()
            distancias[ciudadDestino].getTiempo()
            
            costoTotal = costoTotal + distancias[ciudadDestino].getCosto()
            tiempoTotal = tiempoTotal + distancias[ciudadDestino].getTiempo()

        paretoSet.append([costoTotal,tiempoTotal])

def calcularFrentePareto():
    global paretoSet,frentePareto
    frentePareto = []
    # recorremos el pareto por indices
    for paretoIndex in range( 0,len(paretoSet)):
        # bandera para saber si el pareto con indice paretoIndex no es dominado por otro pareto
        dominado = False
        # ciclo para probar con todos los paretos 
        for paretoIndexAux in range( 0,len(paretoSet)):
            pi = paretoSet[paretoIndex]
            pj = paretoSet[paretoIndexAux]
            # condicion de dominando del pj sobre pi, problema de minimizacion
            if pj[0] <= pi[0] and pj[1] <= pi[1] and ( pj[0] < pi[0] or pj[1] < pi[1]) :
                dominado = True
                break
        # si pareto con indice paretoIndex no es dominado, se agreg al frente pareto
        if not dominado:
            frentePareto.append(paretoSet[paretoIndex])


def imprimirCiudades():
    print("Numero de ciudades:")
    global ciudades
    print("[")
    
    for ciudad in ciudades:
        print("[",end="")
        for ciudadContigua in ciudad:
            # Se imprime de la forma [costo,tiempo]
            ciudadContigua.imprimirCiudad()
            print(end=",")
        print("]")
    print("]")

def imprimirPoblacion():
    global poblacion
    print("Poblacion actual:")
    print("[")
    for cromosoma in poblacion:
        print("[",end="")
        for gen in cromosoma:
            print(gen,end=",")
        print("]")
    print("]")

def imprimirPareto():
    global paretoSet
    print("ParetoSet:")
    print("[")
    for pareto in paretoSet:
        print("[",end="")
        for resultado in pareto:
            print(resultado,end=",")
        print("]")
    print("]")            

def imprimirFrentePareto():
    global frentePareto
    print("Frente pareto:")
    print("[")
    for pareto in frentePareto:
        print("[",end="")
        for resultado in pareto:
            print(resultado,end=",")
        print("]")
    print("]")        

parametros()
generarCiudades()
imprimirCiudades()
generarPoblacionInicial()
imprimirPoblacion()
calcularPareto()
imprimirPareto()
calcularFrentePareto()
imprimirFrentePareto()

'''for iteracion in range(0,iteraciones):
    print("Iteración:",iteracion)
'''
