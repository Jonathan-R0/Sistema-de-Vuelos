#
#   TDA Grafo implementado con listas de adyacencia, (o en este caso
#   diccionario de adyacencia).
#
#   El grafo estará representado de tal forma, que cada vértice estará
#   asociado a un diccionario que contiene a los vértices como claves
#   y pesos como valores asociados.
#
#   Si el vértice 'x' está conectado con el vértice 'y' con una arista de
#   peso 10, esté se estará así representado dentro del diccionario:
#   adyacencias[x] = {... , {y:10} , ...}
#
                    ########################
                    #                      #
                    #      ALGORÍTMOS      #
                    #                      #
                    ########################

import random
import heapq

def quick_sort(lista):
    """Ordena la lista de forma recursiva.
        Pre: los elementos de la lista deben ser comparables.
        Post: la lista está ordenada. """

    _quick_sort(lista, 0, len(lista) - 1)

def _quick_sort(lista, inicio, fin):
    """Función quick_sort recursiva.
        Pre: los índices inicio y fin indican sobre qué porción operar.
        Post: la lista está ordenada."""

    if inicio >= fin:
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
            menores += 1
            if i != menores:
                _swap(lista, i, menores)
    # Ubicar el pivote al final de los menores
    if inicio != menores:
        _swap(lista, inicio, menores)
    return menores

def _swap(lista, i, j):
    """Intercambia los elementos i y j de lista."""
    lista[j], lista[i] = lista[i], lista[j]

def buscar_en_set(conjunto,target1,target2): #SIN TESTEAR
    """DOCUMENTAR"""

    a_devolver = []
    for elemento in conjunto:
        if target1 in elemento or target2 in elemento:
            a_devolver.append(elemento)

    return a_devolver

def kruskal(grafo): #SIN TESTEAR
    """DOCUMENTAR"""

    vertices = []
    vert = grafo.ver_vertices()
    tree = Grafo()

    for v in vert:
        clase_de_eq = set()
        set.add(v)
        vertices.append(set)
        tree.agregar_vertice(v)

    aristas = grafo.ver_aristas_ordenadas()
    for a in aristas:
        a , b , peso = a[0][0] , a[0][1] , a[1]
        for c_eq in vertices:
            clases = buscar_en_set(c_eq,a,b)
            if len(clases) == 1:
                continue
            tree.agregar_arista(a,b,peso)
            clases[0].union(clases[1])

    return tree

# def dijkstra(grafo,origen):
#     dist = {}
#     padres = {}
#     for v in grafo.ver_vertices():
#         dist[v] = float('inf') #Número infinito, siempre es mayor que cualquier otro número
#     dist[origen] = 0
#     padre[origen] = None #INVESTIGAR COMO FUNCIONAN LOS HEAPS DE PYTHON PARA COMPARAR LAS ARISTAS Y ASÍ TERMINAR EL ALGORÍTMO

def _dfs(grafo,v,visitados,padre,orden): #SIN TESTEAR
    """DOCUMENTAR"""

    visitados.add(v)
    ady = grafo.ver_adyacentes(v)
    for tupla in ady:
        w = tupla[0]
        if w not in visitados:
            padre[w] = v
            orden[w] = orden[v] + 1
            dfs(grafo,w,visitados,padre,orden)


def dfs(grafo,origen): #SIN TESTEAR
    """DOCUMENTAR"""

    visitados = set()
    padres = {}
    orden = {}
    padre[origen] = None
    orden[padre] = 0
    _dfs(grafo,origen,visitados,padre,orden)
    return padre, orden

def bfs(grafo,origen): #SIN TESTEAR
    """DOCUMENTAR"""

    visitados = set()
    padres = {}
    orden = {}
    cola = Cola() #IMPLEMENTAR
    visitados.agregar(origen)
    padres[origen] = None
    orden[origen] = 0
    cola.encolar(origen)

    while !cola.esta_vacia():
        v = cola.desencolar()
        for tupla in grafo.ver_adyacentes(v):
            w = tupla[0]
            if w not in visitados:
                visitados.agregar(w)
                padre[w] = v
                orden[w] = orden[v] + 1
                cola.encolar(w)

    return padre,orden



                    ########################
                    #                      #
                    #        OBJETO        #
                    #                      #
                    ########################

class Grafo:

    def __init__(self):

        self.vertices = 0
        self.aristas = 0
        self.adyacencias = {}

    def __str__(self):
        return str(self.adyacencias)

    def __contains__(self,x):
        """ Verifica que el vértice 'x' esté en el grafo. Opera en O(1). """

        return x in self.adyacencias

    def ver_adyacencia(self,x,y):
        """ Devuelve true si el vértice se encuentra en el grafo, false en
        caso contrario. Opera en O(1). """

        if (x in self.adyacencias) and (y in self.ayacencias[0]):
            return True
        return False

    def ver_adyacentes(self,x):
        """ Devuelve una lista con todas tuplas vértice-peso asociadas
        al arista 'x' pasado por parámetro. En el peor caso es O(|V|). """

        ady = []

        if x in self.adyacencias:
            ady = list(self.adyacencias[x].items())

        return ady

    def agregar_vertice(self,x):
        """ Añade el vértice 'x' al diccionario de vértices, en caso de no estar.
        En un principio este está desconectado del resto de vértices. Si
        el vértice ya estaba en el grafo devuelve False. Opera en O(1) pues
        al principio está desconectado. """

        if x not in self.adyacencias:
            self.adyacencias[x] = {}
            self.vertices += 1
            return True

        return False

    def sacar_vertice(self,x):
        """ Quita el vértice del grafo. Primero quita la fila que corresponde a la
        posición de 'x' en el diccionario. Luego elimina las aristas asociadas.
        Opera en O(|V| + |E|). """

        muertos = None

        if x in self.adyacencias:
            muertos = self.adyacencias.pop(x)
            for ady in muertos:
                if ady in self.adyacencias:
                    self.adyacencias[ady].pop(x)

        self.aristas -= len(muertos)
        self.vertices -= 1
        return list(muertos.items())

    def agregar_arista(self,x,y,peso):
        """ Agrega una arista que conecta a los vértices 'x' y 'y', en caso
        de que estén dentro del grafo. Si alguno de los vértices no
        estaba en el grafo se devuelve False o True cuando la operación
        se ejecuta exitosamente. Opera en O(|V|) en el peor caso. """

        if (x in self.adyacencias) and (y in self.adyacencias):
            self.adyacencias[x][y] = peso
            self.adyacencias[y][x] = peso
            self.aristas += 1
            return True

        return False

    def remover_arista(self,x,y):
        """ Quita la arista que conecta a los vértices pasados por parámetro
        en caso que se encuentren dentro del grafo. Opera en O(|V|) en el
        peor caso. """

        resultado = None

        if (x in self.adyacencias) and (y in self.adyacencias):
            resultado = self.adyacencias[x].pop(y)
            self.aristas -= 1
            if (y != x):
                self.adyacencias[y].pop(x)

        return resultado

    def ver_peso(self,x,y):
        """ Devuelve el peso de la arista que conecta a los vértices pasados
        por parámetro en caso que se encuentren dentro del grafo. Es O(1). """

        peso = None

        if (x in self.adyacencias) and (y in self.adyacencias[x]):
            peso = self.adyacencias[x][y]

        return peso

    def cambiar_peso(self,x,y,peso):
        """ Cambia el peso de la arista que conecta a los vértices pasados
        por parámetro en caso que se encuentren dentro del grafo. Es O(1).
        Si alguno de los vértices no estaba en el grafo se
        devuelve False o True cuando la operación se ejecuta exitosamente. """

        if (x in self.adyacencias) and (y in self.adyacencias[x]):
            self.adyacencias[x][y] = peso
            self.adyacencias[y][x] = peso
            return True

        return False

    def esta_vacio(self):
        """ Devuelve True si está vacío, False en caso contrario, en O(1). """

        return self.vertices == 0

    def ver_vertices(self):
        """Devuelve una lista con todos los vértices."""

        return [*self.adyacencia]

    def vertice_aleatorio(self):
        """En caso de no estar vacío el grafo, devuelve un vértice random.
        De lo contrario devuelve 'None'."""

        if self.vertices == 0:
            return random.choice(self.adyacencia)
        return None

    def ver_aristas(self):
        """Devuelve un diccionario con su clave siendo la tupla formada por
        un par de vértices y la clave es el peso que las conecta."""

        resultado = {}
        for v in self.adyacencias:
            for w in self.adyacencias[v]:
                if (w,v) not in resultado:
                    resultado[v,w] = self.adyacencias[v][w]

        return list(resultado.items())

    def ver_aristas_ordenadas(self):
        """Devuelve un diccionario con su clave siendo la tupla formada por
        un par de vértices y la clave es el peso que las conecta. Está ordenado
        de menor a mayor peso. Opera en O(|E|*log(|E|))."""

        copia = self.ver_aristas()
        quick_sort(copia)
        return copia

    def cantidad_aristas(self):
        """Devuelve la cantidad de aristas en O(1)."""
        return self.aristas

    def cantidad_vertices(self):
        """Devuelve la cantidad de vértices en O(1)."""
        return self.vertices

                    ########################
                    #                      #
                    #        TESTS         #
                    #                      #
                    ########################


grafo = Grafo()
print(grafo)

grafo.agregar_vertice('a')
grafo.agregar_vertice('b')
grafo.agregar_arista('a','b',10)
print(grafo)

grafo.agregar_arista('b','a',50)
print(grafo)

print(grafo.ver_peso('a','b'))

grafo.cambiar_peso('b','a',100)
print(grafo.ver_peso('a','b'))

grafo.cambiar_peso('a','b',0)
print(grafo.ver_peso('a','b'))
print(grafo)

grafo.agregar_vertice('c')
grafo.agregar_arista('c','c',99)
print(grafo)

grafo.agregar_arista('c','b',1)
grafo.agregar_arista('c','a',2)
print(grafo)

print(grafo.ver_adyacentes('a'))

print("TEST\n\n")
oh_shid = grafo.ver_aristas()
print(oh_shid)
print(grafo.ver_aristas_ordenadas())
print("\n\nTEST")

print(grafo)

grafo.sacar_vertice('c')
print(grafo)

grafo.agregar_arista('b','a',50)
print(grafo)

grafo.cambiar_peso('b','a',100)
print(grafo)

print(grafo.ver_aristas())
