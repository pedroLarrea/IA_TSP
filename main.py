import random
import math
import numpy as np
import sys


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
proximaPoblacion = []
# pareto {CostoTotal, tiempoTotal}
paretoSet = []
frentePareto = []
dominados = []

# Datos varios
# Cantidad de iteraciones(maximo)
iteraciones = 1

'''
    si nroCiudades = 3

    ciudades[nroCiudades][nroCiudades] = { 
                    { [1,3], [4,2], [3,0]},
                    { [5,2], [1,3], [8,2] },
                    { [2,1], [3,5], [9,2] }
                    };

'''

def parametros():
    global nroCiudades,maxCosto,maxTiempo,tamanhoPoblacion,iteraciones
    
    print ("Introduce el numero de ciudades:")
    nroCiudades = int(input()) + 1
    print ("Introduce costo maximo entre ciudades:")
    maxCosto = int(input())
    print ("Introduce tiempo maximo entre ciudades:")
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
    global paretoSet, ciudades, poblacion, tamanhoPoblacion
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
    global paretoSet, frentePareto, dominados, poblacion
    frentePareto = []
    dominados = []
    print("Calculando frente pareto...")
    # recorremos el pareto por indices
    for paretoIndex in range( 0, len(poblacion)):
        # bandera para saber si el pareto con indice paretoIndex no es dominado por otro pareto
        dominado = False
        # ciclo para probar con todos los paretos 
        for paretoIndexAux in range( 0, len(poblacion)):
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
    global frentePareto, poblacion
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
    
def sumaColumna(matriz, indice):
    answer = 0
    # axis=-1 es "suma de la ultima columna"
    for cromosoma in matriz:
        answer += cromosoma[indice]
    return answer


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

def elitista():
    global poblacion, proximaPoblacion
    porcentajeElitista = 0.4
    cantElementElitista = math.ceil(porcentajeElitista*len(poblacion))
    poblacionAux = poblacion
    elegidos = []
    sumatoria = sumaColumna(poblacion, -1)
    target = round(random.uniform(0.00, sumatoria), 15)
    limite = 100
    inicial = 0
    loop=0
    while(len(elegidos)<cantElementElitista and loop<limite):
        for c in poblacionAux:
            inicial += c[-1]
            if(inicial >= target):
                elegidos.append(c)
                inicial -= c[-1]
                #Analizar si el ciclo sigue sin problemas
                poblacionAux.remove(c)
                sumatoria = sumaColumna(poblacionAux, -1)
                target = round(random.uniform(0.00, sumatoria), 15)
                break
        loop=loop+1
    print("Cant. de poblacion elegida por Elitista ", len(elegidos))
    print("Cant. de poblacion a mutar ", len(poblacionAux))
    poblacion = poblacionAux
    proximaPoblacion = elegidos
    
def mutacion():
    global poblacion, proximaPoblacion
    rand1 = 0
    rand2 = 0
    for c in poblacion:
        rand1 = rand2 = random.randint(1, nroCiudades-1)
        while(rand1 == rand2):
            rand2 = random.randint(1, nroCiudades-1)
        #Invertimos lugares para generar la mutacion
        aux = c[rand1]
        c[rand1] = c[rand2]
        c[rand2] = aux
    '''calcularPareto()
    calcularFrentePareto()
    calcularFitness()'''
def invertirFitness():
    global poblacion
    for c in poblacion:
        c[-1] = 1 / c[-1]
    
def eliminarUltimasColumnas(target):
    #Eliminamos sumatoria de costo y tiempo viejo, y fitness
    for c in target:
        c.pop(-1)
        c.pop(-1)
        
# 1er paso introducir parametros
parametros()

# Archivo para exportar la salida
path = 'SPEA.txt'
sys.stdout = open(path, 'w')

# 2do paseo: generación automatica de ciudades, costos y tiempo
generarCiudades()
imprimirCiudades()

# se genera problacion inicial
generarPoblacionInicial()
# imprimirPoblacion("Poblacion Inicial")
i = 0
while(i<=iteraciones): 
    print("##############################################################################")
    print("                             ITERACION ", i+1,"                               ")
    print("##############################################################################")
    
    imprimirPoblacion("La poblacion es:")
    # Calculamos el pareto de los cromosoma (suma de costos y tiempo de cada cromosoma)
    calcularPareto()
    # calculamos el frente pareto (paretos no dominados)
    calcularFrentePareto()

    # calculasmos el fitness para el siguiente paso genetico
    calcularFitness()
    invertirFitness()
    # imprimirPoblacion("Poblacion con pareto y fitness:")
    poblacion = sorted(poblacion, key=lambda x: x[-1])
    imprimirPoblacion("Poblacion Ordenada con pareto y fitness:")
    elitista()
    eliminarUltimasColumnas(poblacion)
    mutacion()
    eliminarUltimasColumnas(proximaPoblacion)
    #Se unen valores formados por la estrategia elitista y mutacion
    poblacion = proximaPoblacion + poblacion
    proximaPoblacion = []
    i = i+1
    imprimirPoblacion("La poblacion final es:")
    
