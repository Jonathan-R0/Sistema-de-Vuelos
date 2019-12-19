#!/usr/bin/python3
from grafo import Grafo
from biblioteca import _vacaciones
from biblioteca import centralidad_aproximada
from biblioteca import centralidad_betweeness
from biblioteca import prim
from biblioteca import bfs
from biblioteca import dijkstra
from random import choice
from sys import stdin
from sys import argv
import operator

                    ########################
                    #                      #
                    #       PROGRAMA       #
                    #                      #
                    ########################


CANT_CAMINOS_CENT_APROX = 100
LARGO_CAMINOS_CENT_APROX = 100
LISTAR_OPS = "listar_operaciones"
CAMINO = "camino_mas"
ESCALAS = "camino_escalas"
VACACIONES = "vacaciones"
NUEVA_AEROLINEA = "nueva_aerolinea"
CENT_TOTAL = "centralidad"
CENT_APROX = "centralidad_aprox"
COMANDOS = [CAMINO,ESCALAS,CENT_TOTAL,CENT_APROX,NUEVA_AEROLINEA,VACACIONES]
ESPACIO = ' '
COMA = ','
OP1 = "barato"
OP2 = "rapido"
MODO_LECTURA = 'r'
MODO_ESCRITURA = "w"
FLECHA = " -> "
ERROR_VACACIONES = "No se encontro recorrido"
COMA2 = ", "

def listar_op():
    """Imprime en O(1) la lista de operaciones disponibles."""
    for i in range(len(COMANDOS)):
        print(COMANDOS[i])

def imprimir_centralidad(centralidad,n):
    respuestas = []
    for i in range(n):
        maximo = max(centralidad.items(),key=operator.itemgetter(1))
        centralidad.pop(maximo[0])
        respuestas.append(maximo[0])
    print((COMA2).join(respuestas))

def centrality_aprox(grafo,n):
    centralidad = centralidad_aproximada(grafo,CANT_CAMINOS_CENT_APROX,LARGO_CAMINOS_CENT_APROX)
    imprimir_centralidad(centralidad,n)

def centrality_total(grafo,n):
    centralidad = centralidad_betweeness(grafo)
    imprimir_centralidad(centralidad,n)

def new_aerolinea(grafo1,grafo2,grafo3,ruta_archivo):
   mst = prim(grafo2)
   escribir_archivo(grafo1,grafo2,grafo3,mst,ruta_archivo)
   print("OK")

def escribir_archivo(grafo1,grafo2,grafo3,mst,ruta_archivo):
    """Exporta un archivo con todas las rutas necesarias para crear una nueva aerolinea
    que se pueda comunicar con todos los aeropuertos."""
    aristas = mst.ver_aristas()
    with open(ruta_archivo,MODO_ESCRITURA) as f:
        for i in range(len(aristas)):
            linea = f"{aristas[i][0][0]},{aristas[i][0][1]},{grafo1.ver_peso(aristas[i][0][0],aristas[i][0][1])},{grafo2.ver_peso(aristas[i][0][0],aristas[i][0][1])},{grafo3.ver_peso(aristas[i][0][0],aristas[i][0][1])}"
            f.write(linea+"\n")

def leer_archivo(aeropuertos,vuelos):
    """Lee el archivo de aeropuertos y vuelos, y crea los grafos y estructuras necesarias para que funcione el programa."""
    data = []
    cities = {} #Diccionario donde me guardo como clave una ciudad y como valor una lista con los aeropuertos
    flights = {} #Diccionario donde me guardo como clave un aeropuerto y com valor la ciudad a la que pertenece

    grafo_tiempo = Grafo()
    grafo_precio = Grafo()
    grafo_freq = Grafo()
    grafo_freq2 = Grafo()

    with open(aeropuertos,MODO_LECTURA) as file1:
        for linea in file1:

            linea = (linea.rstrip()).split(COMA)

            grafo_tiempo.agregar_vertice(linea[1])
            grafo_precio.agregar_vertice(linea[1])
            grafo_freq.agregar_vertice(linea[1])
            grafo_freq2.agregar_vertice(linea[1])

            if linea[0] not in cities:
                cities[linea[0]] = [linea[1]]
            else:
                cities[linea[0]].append(linea[1])

            flights[linea[1]] = linea[0]

    with open(vuelos,MODO_LECTURA) as file2:
        for linea in file2:

            linea = (linea.rstrip()).split(COMA)

            grafo_tiempo.agregar_arista(linea[0],linea[1],int(linea[2]))
            grafo_precio.agregar_arista(linea[0],linea[1],int(linea[3]))
            grafo_freq.agregar_arista(linea[0],linea[1],int(linea[4]))
            grafo_freq2.agregar_arista(linea[0],linea[1],1/int(linea[4]))


    return grafo_tiempo, grafo_precio, grafo_freq, grafo_freq2, cities, flights

def vacaciones(grafo,cities,origen,n):
    if n < 1 or (origen not in cities):
        print(ERROR_VACACIONES)
        return

    for aerop in cities[origen]:
        visitados = set()
        rta = _vacaciones(grafo,n - 1,aerop,[],aerop,visitados)
        if len(rta) == 0:
            continue
        else:
            break

    if len(rta) == 0:
        print(ERROR_VACACIONES)
    else:
        print(FLECHA.join([aerop]+rta+[aerop]))
    return

def imprimir_camino(padres,min_indice,min_ciudad,distancias):
    """Imprime, dado el diccionario de padres y distancias, la respuesta al camino deseado."""
    padre = padres[min_indice]
    distancia = distancias[min_indice]

    rta = [min_ciudad]

    prox = min_ciudad
    while prox != None:
        rta.append(padre[prox])
        prox = padre[prox]
    if rta[-1] == None: rta.pop()

    print(FLECHA.join(rta[::-1]))

def camino_escalas(grafo,ciudad_origen,ciudad_destino,cities,flights):
    padres = []
    ordenes = []
    primer_interceptado = []

    for aeropuerto in cities[ciudad_origen]:

        w,padre,orden = bfs(grafo,aeropuerto,cities[ciudad_destino])

        primer_interceptado.append(w)
        padres.append(padre)
        ordenes.append(orden)

    contador = 0
    min_indice = 0
    min = float('inf')
    for interceptado in primer_interceptado:
        if int(ordenes[contador][interceptado]) < min:
            min = int(ordenes[contador][interceptado])
            min_indice = contador
        contador += 1

    llegada = primer_interceptado[min_indice]

    imprimir_camino(padres,min_indice,llegada,ordenes)

def camino_mas(cities,grafo,salida,llegada):
    padres = []
    distancias = []

    for aeropuerto in cities[salida]:
        padre,distancia,distancia_a_ciudad = dijkstra(grafo,aeropuerto,cities[llegada])
        padres.append(padre)
        distancias.append(distancia)

    contador = 0
    min_ciudad = 0
    min = float('inf')
    for ciudad in distancia_a_ciudad:
        if int(distancia_a_ciudad[ciudad]) < min:
            min = int(distancia_a_ciudad[ciudad])
            min_ciudad = ciudad

    min_indice = 0

    for diccionario in distancias:
        if int(diccionario[min_ciudad]) == min:
            min_indice = contador
            break
        contador += 1

    imprimir_camino(padres,min_indice,min_ciudad,distancias)

def main():
    """Funcion principal del programa. Recibe los grafos. Es el esqueleto del resto de funciones que son llamadas dentro de esta."""
    aeropuertos = argv[1]
    vuelos = argv[2]
    grafo_tiempo, grafo_precio, grafo_freq, grafo_freq2,cities, flights = leer_archivo(aeropuertos,vuelos)
    for line in stdin:
        line = (line.rstrip()).split(ESPACIO)
        determinante = line[0]

        if determinante == LISTAR_OPS:
            listar_op()
            continue

        if determinante == NUEVA_AEROLINEA:
            new_aerolinea(grafo_tiempo,grafo_precio,grafo_freq,line[1])
            continue

        info = (ESPACIO.join(line[1::])).split(COMA)

        if determinante == CAMINO:
            if (len(info) != 3): continue
            if info[0] == OP1: camino_mas(cities,grafo_precio,info[1],info[2])
            elif info[0] == OP2: camino_mas(cities,grafo_tiempo,info[1],info[2])
            continue

        elif determinante == ESCALAS:
            if len(info) != 2: continue
            camino_escalas(grafo_tiempo,info[0],info[1],cities,flights)

        elif determinante == VACACIONES:
            if (len(info) != 2 or not info[-1].isdigit()): continue
            vacaciones(grafo_tiempo,cities,info[0],int(info[1]))

        if (len(info) != 1 or not info[0].isdigit()): continue

        if determinante == CENT_TOTAL:
            centrality_total(grafo_freq2,int(info[0]))
            continue

        elif determinante == CENT_APROX:
            centrality_aprox(grafo_freq,int(info[0]))

main()
