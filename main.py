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
dominados = []

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
    print("Calculando Pareto...")
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

        cromosoma.append([costoTotal,tiempoTotal])

def calcularFrentePareto():
    global paretoSet,frentePareto,dominados,poblacion
    frentePareto = []
    dominados = []
    print("Calculando frente pareto...")
    # recorremos el pareto por indices
    for paretoIndex in range( 0,len(poblacion)):
        # bandera para saber si el pareto con indice paretoIndex no es dominado por otro pareto
        dominado = False
        # ciclo para probar con todos los paretos 
        for paretoIndexAux in range( 0,len(poblacion)):
            pi = poblacion[paretoIndex]
            pj = poblacion[paretoIndexAux]
            # condicion de dominando del pj sobre pi, problema de minimizacion
            if pj[-1][0] <= pi[-1][0] and pj[-1][1] <= pi[-1][1] and ( pj[-1][0] < pi[-1][0] or pj[-1][1] < pi[-1][1]) :
                dominado = True
                break
        # si pareto con indice paretoIndex no es dominado, se agreg al frente pareto
        if not dominado:
            frentePareto.append(poblacion[paretoIndex])
        else:
            dominados.append(poblacion[paretoIndex])

def calcularFitness():
    global frentePareto,poblacion
    print("Calculando fitness...")
    # calculamos fitness para frente pareto

    # se va a recrear la poblacion con la mezcla de el frente pareto y los no dominados a fin de tener todos los en una sola estructura
    poblacion = []

    for frenteParetoInd in range(0,len(frentePareto)):
        count = 0
        for popInd in dominados:
            # verificamos si el elemento del frente pareto cubre a popInd
            if frentePareto[frenteParetoInd][-1][0] <= popInd[-1][0] and frentePareto[frenteParetoInd][-1][1] <= popInd[-1][1]:
                count += 1
        strength = count / (len(dominados) + 1)
        frentePareto[frenteParetoInd].append(strength)
        # se carga en la poblacion
        poblacion.append(frentePareto[frenteParetoInd])

    # calculamos el fitness para los dominados
    for dominadoInd in range(0,len(dominados)):
        sum = 0
        for popInd in frentePareto:
            # verificamos si el elemento del frente pareto cubre al elemento dominado
            if dominados[dominadoInd][-1][0] >= popInd[-2][0] and dominados[dominadoInd][-1][1] >= popInd[-2][1]:
                sum += popInd[-1]
        strength = sum + 1
        dominados[dominadoInd].append(strength)
        # se carga en la poblacion
        poblacion.append(dominados[dominadoInd])

# def seleccion():
    # 40% por el metodo elitista

    # 60% por mutacion
    

def imprimirCiudades():
    print("Lista de ciudades iudades:")
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

def imprimirPoblacion(titulo):
    global poblacion
    print(titulo)
    print("[")
    for cromosoma in poblacion:
        print("[",end="")
        for gen in cromosoma:
            print(gen,end=",")
        print("]")
    print("]") 

# 1er paso introducir parametros
parametros()

# 2do paseo: generación automatica de ciudades, costos y tiempo
generarCiudades()
imprimirCiudades()

# se genera problacion inicial
generarPoblacionInicial()
imprimirPoblacion("Poblacion Inicial")

# Calculamos el pareto de los cromosoma (suma de costos y tiempo de cada cromosoma)
calcularPareto()

# calculamos el frente pareto (paretos no dominados)
calcularFrentePareto()

# calculasmos el fitness para el siguiente paso genetico
calcularFitness()
imprimirPoblacion("Poblacion con pareto y fitness:")

'''for iteracion in range(0,iteraciones):
    print("Iteración:",iteracion)
'''
