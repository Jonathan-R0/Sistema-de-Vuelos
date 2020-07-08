import random
import heapq
import operator
from grafo import Cola
from grafo import Grafo

                    ########################
                    #                      #
                    #      ALGORÍTMOS      #
                    #                      #
                    ########################


def quick_sort(lista):
    """Ordena la lista de forma recursiva.
        Pre: los elementos de la lista deben ser comparables.
        Post: la lista está ordenada. """

    _quick_sort(lista, 0, len(lista) - 1)

def _quick_sort(lista, inicio, fin):
    """Función quick_sort recursiva.
        Pre: los índices inicio y fin indican sobre qué porción operar.
        Post: la lista está ordenada."""

    if inicio >=  fin:
        return
    menores = _partition(lista, inicio, fin)
    _quick_sort(lista, inicio, menores - 1)
    _quick_sort(lista, menores + 1, fin)


def _partition(lista, inicio, fin):
    """Función partición que trabaja sobre la misma lista.
        Pre: los índices inicio y fin indican sobre qué porción operar.
        Post: los menores están antes que el pivote, los mayores después.
        Devuelve: la posición en la que quedó ubicado el pivote."""

    pivote = lista[inicio]
    menores = inicio

    # Ubicar menores a la izquierda, mayores a la derecha
    for i in range(inicio + 1, fin + 1):
        if lista[i][1] < pivote[1]:
            menores +=  1
            if i !=  menores:
                _swap(lista, i, menores)
    # Ubicar el pivote al final de los menores
    if inicio !=  menores:
        _swap(lista, inicio, menores)
    return menores

def _swap(lista, i, j):
    """Intercambia los elementos i y j de lista."""
    lista[j], lista[i] = lista[i], lista[j]

def dijkstra(grafo,origen,destino=[]):
    """Este algorítmo devuelve un diccionario de padres y distancias
    correspondientes al resultado del algorítmo de Dijkstra.
    Pre: recibe un grafo válido y un vértice de origen válido.
    Opera en O(|E|*log(|E|))."""

    dist = {}
    padre = {}
    dist_llegada = {}
    for v in grafo.ver_vertices():
        dist[v] = float('inf') # Infinito, siempre es mayor que cualquier otro número
        if v in destino:
            dist_llegada[v] = float('inf')
    dist[origen] = 0
    padre[origen] = None
    heap = []
    heapq.heappush(heap,(0,origen))
    while heap:
        arista = heapq.heappop(heap) #(peso_hasta_a,'v')
        v = arista[1]
        for w in grafo.ver_a_adyacentes(v):
            w = w[0]
            if dist[v] + grafo.ver_peso(w,v) < dist[w]:
                dist[w] = dist[v] + grafo.ver_peso(w,v)
                if w in destino: dist_llegada[w] = dist[w]
                padre[w] = v
                heapq.heappush(heap,(dist[w],w))


    return padre,dist,dist_llegada


def prim(grafo):
    """Algoritmo de prim para obtener el arbol de tendido minimo de un grafo."""

    vertice = grafo.vertice_aleatorio()
    vert = grafo.ver_vertices()
    visitados = set()
    visitados.add(vertice)
    heap = []
    arbol = Grafo()
    for v in vert:
        arbol.agregar_vertice(v)
    for w in grafo.ver_v_adyacentes(vertice):
        heapq.heappush(heap,(grafo.ver_peso(vertice,w),(vertice,w)))
    while len(heap)>0:
        (peso,(v,w)) = heapq.heappop(heap)
        if w in visitados:
            continue
        arbol.agregar_arista(v,w,peso)
        visitados.add(w)
        for u in grafo.ver_v_adyacentes(w):
            if u not in visitados:
                heapq.heappush(heap,(grafo.ver_peso(w,u),(w,u)))
    return arbol


def _dfs(grafo,v,visitados,padre,orden): #SIN TESTEAR

    visitados.add(v)
    ady = grafo.ver_a_adyacentes(v)
    for tupla in ady:
        w = tupla[0]
        if w not in visitados:
            padre[w] = v
            orden[w] = orden[v] + 1
            _dfs(grafo,w,visitados,padre,orden)


def dfs(grafo,origen): #SIN TESTEAR
    """Recorrido dfs (profundidad) sobre un grafo. Devuelve el diccionario de padres y orden. Opera en
    O(E+V)"""

    visitados = set()
    padres = {}
    orden = {}
    padre[origen] = None
    orden[origen] = 0
    _dfs(grafo,origen,visitados,padre,orden)
    return padre, orden

def bfs(grafo,origen,destino=[]): #SIN TESTEAR
    """Recorrido bfs sobre un grafo(ancho). Devuelve el diccionario de padres y orden. Opera en
    O(V+E)"""

    visitados = set()
    padres = {}
    orden = {}
    cola = Cola()
    visitados.add(origen)
    padres[origen] = None
    orden[origen] = 0
    cola.encolar(origen)

    while not cola.esta_vacia():
        v = cola.desencolar()
        for tupla in grafo.ver_a_adyacentes(v):
            w = tupla[0]
            if w not in visitados:
                visitados.add(w)
                padres[w] = v
                orden[w] = orden[v] + 1
                cola.encolar(w)
                if w in destino:
                    return w,padres,orden

    return None,padres,orden

def pesos_ady(grafo,vertice):
    """Dado un grafo y un vertice devuelve un diccionario con los vertices adyacentes
    como clave y el peso de la arista como valor"""

    diccionario = {}
    adyacentes = grafo.ver_a_adyacentes(vertice)
    for a in adyacentes:
        diccionario[a[0]] = a[1]
    return diccionario

def vertice_aleatorio(pesos):
    """Obtiene un vertice aleatorio de un diccionario de vertices y pesos, dando prioridad a los
    pesos mayores"""
    total = sum(pesos.values())
    rand = random.uniform(0, total)
    acum = 0
    for vertice, peso_arista in pesos.items():
        if acum + peso_arista >=  rand:
            return vertice
        acum +=  peso_arista


def centralidad_aproximada(grafo,cant_caminos,largo_camino):
    """Nos muestra los n aeropuertos más centrales/importantes del mundo,
    de mayor importancia a menor importancia."""
    centralidad = {}
    vertices = grafo.ver_vertices()
    for v in vertices:
        centralidad[v] = 0
    vertice = grafo.vertice_aleatorio()
    for i in range (cant_caminos):
        for j in range (largo_camino):
            vertice = vertice_aleatorio(pesos_ady(grafo,vertice))
            centralidad[vertice]+= 1
    return centralidad

def centralidad_betweeness(grafo):
    """Nos muestra los n aeropuertos más centrales/importantes del mundo,
    de forma aproximada, de mayor importancia a menor importancia."""
    cent = {}
    vertices = grafo.ver_vertices()
    for v in vertices:
        cent[v] = 0
    for v in vertices:
        # hacia todos los demas vertices
        padre,distancia,x = dijkstra(grafo, v)
        cent_aux = {}
        for w in vertices:
            cent_aux[w] = 0
        # Aca filtramos (de ser necesario) los vertices a distancia infinita,
        # y ordenamos de mayor a menor
        distancias=list(distancia.items())
        quick_sort(distancias)
        for i in range (len(distancias)-1,-1,-1):
            if padre[distancias[i][0]]!=None:
                cent_aux[padre[distancias[i][0]]] +=  1 + cent_aux[distancias[i][0]]
        # le sumamos 1 a la centralidad de todos los vertices que se encuentren en
        # el medio del camino
        for w in vertices:
            if w ==  v: continue
            cent[w] +=  cent_aux[w]
    return cent

def _vacaciones(grafo,n,v,solucion,origen,visitados):
    """Obtiene un ciclo de largo n desde un origen que se pasa por
    parametro."""
    visitados.add(v)
    if (len(solucion) == n):
        if origen in grafo.ver_v_adyacentes(v):
            return solucion
        else:
            visitados.remove(v)
            return []
    for w in grafo.ver_v_adyacentes(v): #FALTA PODAR CON VISITADOS
        if w in visitados: continue
        sol = _vacaciones(grafo,n,w,solucion+[w],origen,visitados)
        if (len(sol) == n):
            return sol
    visitados.remove(v)
    return []
