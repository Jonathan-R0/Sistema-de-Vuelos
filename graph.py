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
                    #        OBJETO        #
                    #                      #
                    ########################

class Cola:

    def __init__(self):
        self.items = []

    def encolar(self,x):
        """Mete un elemento en la estructura. Opera en O(1)."""

        self.items.append(x)

    def desencolar(self):
        """Saca un elemento de la estructura en O(1). En caso de
        estar vacía, devuelve el error correspondiente."""

        if self.esta_vacia():
            raise ValueError("La cola no tiene elementos.")
        return self.items.pop(0)

    def esta_vacia(self):
        """Devuelve True si está vacía la cola, False en caso contrario;
        todo en O(1)."""

        return len(self.items) ==  0

    def ver_primero(self):
    	"""Devuelve el primer elemento, si existe"""
    	if self.esta_vacia():
    		raise ValueError("La cola no tiene elementos.")
    	return self.items[0]

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
        """ Devuelve true 2 vertices son adyacentes, false en
        caso contrario. Opera en O(1). """

        if (x in self.adyacencias) and (y in self.adyacencias[x]):
            return True
        return False

    def ver_a_adyacentes(self,x):
        """ Devuelve una lista con todas tuplas vértice-peso asociadas
        al vertice 'x' pasado por parámetro. En el peor caso es O(|V|). """

        ady = []

        if x in self.adyacencias:
            ady = list(self.adyacencias[x].items())

        return ady

    def ver_v_adyacentes(self,x):
        """Devuelve una lista con los vertices adyacentes al pasado por
        parametro"""
        ady = []

        if x in self.adyacencias:
            ady = list(self.adyacencias[x].keys())

        return ady

    def agregar_vertice(self,x):
        """ Añade el vértice 'x' al diccionario de vértices, en caso de no estar.
        En un principio este está desconectado del resto de vértices. Si
        el vértice ya estaba en el grafo devuelve False. Opera en O(1) pues
        al principio está desconectado. """

        if x not in self.adyacencias:
            self.adyacencias[x] = {}
            self.vertices +=  1
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

        self.aristas -=  len(muertos)
        self.vertices -=  1
        return list(muertos.items())

    def agregar_arista(self,x,y,peso):
        """ Agrega una arista que conecta a los vértices 'x' y 'y', en caso
        de que estén dentro del grafo. Si alguno de los vértices no
        estaba en el grafo se devuelve False o True cuando la operación
        se ejecuta exitosamente. Opera en O(|V|) en el peor caso. """

        if (x in self.adyacencias) and (y in self.adyacencias):
            self.adyacencias[x][y] = peso
            self.adyacencias[y][x] = peso
            self.aristas +=  1
            return True

        return False

    def remover_arista(self,x,y):
        """ Quita la arista que conecta a los vértices pasados por parámetro
        en caso que se encuentren dentro del grafo. Opera en O(|V|) en el
        peor caso. """

        resultado = None

        if (x in self.adyacencias) and (y in self.adyacencias):
            resultado = self.adyacencias[x].pop(y)
            self.aristas -=  1
            if (y !=  x):
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

        return self.vertices ==  0

    def ver_vertices(self):
        """Devuelve una lista con todos los vértices."""

        return [*self.adyacencias]

    def vertice_aleatorio(self):
        """En caso de no estar vacío el grafo, devuelve un vértice random.
        De lo contrario devuelve 'None'."""

        if self.vertices > 0:
            return random.choice(list(self.adyacencias.keys()))
        return None

    def ver_aristas(self):
        """Devuelve una lista con su 'clave' siendo la tupla formada por
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
                    #      ALGORÍTMOS      #
                    #                      #
                    ########################

import random
import heapq
import operator

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


def dijkstra(grafo,origen):
    """Este algorítmo devuelve un diccionario de padres y distancias
    correspondientes al resultado del algorítmo de Dijkstra.
    Pre: recibe un grafo válido y un vértice de origen válido.
    Opera en O(|E|*log(|E|))."""

    dist = {}
    padre = {}
    for v in grafo.ver_vertices():
        dist[v] = float('inf') #Número infinito, siempre es mayor que cualquier otro número
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
                padre[w] = v
                heapq.heappush(heap,(dist[w],w))

    return padre,dist

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

def bfs(grafo,origen): #SIN TESTEAR
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

    return padres,orden

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
    """Recibe un grafo, una cantidad de caminos a realizar y un largo y devuelve un diccionario
    con la centralidad aproximada de que cada vertice"""
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
    cent = {}
    vertices = grafo.ver_vertices()
    for v in vertices:
        cent[v] = 0
    for v in vertices:
        # hacia todos los demas vertices
        padre,distancia = dijkstra(grafo, v)
        
        cent_aux = {}
        for w in vertices:
            cent_aux[w] = 0
        # Aca filtramos (de ser necesario) los vertices a distancia infinita,
        # y ordenamos de mayor a menor
        distancias=list(distancia.items())
        quick_sort(distancias)
        print(f"Para{v} las padres son {padre}")
        print(f"Para{v} las distancias son {distancias}")
        

        for i in range (len(distancias)-1,-1,-1):
            if padre[distancias[i][0]]!=None:
                cent_aux[padre[distancias[i][0]]] +=  1 + cent_aux[distancias[i][0]]
        print(f"La cent aux es{cent_aux}")
        # le sumamos 1 a la centralidad de todos los vertices que se encuentren en
        # el medio del camino
        for w in vertices:
            if w ==  v: continue
            cent[w] +=  cent_aux[w]
    return cent

def _vacaciones(grafo,n,v,solucion,origen,visitados):
    #print("Por ahora el resultado es:",solucion)
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

def vacaciones(grafo,origen,n):
    visitados = set()
    return _vacaciones(grafo,n,origen,[],origen,visitados)

def buscar_proximo(grafo,v,visitados):
    aristas = grafo.ver_a_adyacentes(v);
    quick_sort(aristas)
    print("Los adyacentes ordenados son: ",aristas,"y los visitados: ",visitados)
    min = aristas[0] #Si el primero fue visitado no lo agarra
    for arista in aristas:
        if arista[0] not in visitados:
            return arista[0],arista[1]

    return min[0],min[1]


def _global(grafo,v,visitados,solucion,peso):
    print("Por ahora la solución es: ",solucion,"y el peso es:",peso,"\n")
    visitados.add(v)
    if len(visitados) == len(grafo.ver_vertices()):
        return solucion , peso
    w , peso_parcial = buscar_proximo(grafo,v,visitados)
    return _global(grafo,w,visitados,solucion+[w],peso+peso_parcial)


def global_greedy(grafo,origen): #Para recorrer el mundo aprox
    visitados = set()
    visitados.add(origen)
    solucion = [origen]
    return _global(grafo,origen,visitados,solucion,0)


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

print(grafo.ver_a_adyacentes('a'))

print("TEST ARISTAS ORDENADAS\n\n")
oh_shid = grafo.ver_aristas()
print(oh_shid)
print(grafo.ver_aristas_ordenadas())
print("\n\nTEST ARISTAS ORDENADAS")

print("TEST DIJKSTRA\n\n")
padre , distancia = dijkstra(grafo,'a')
print("Padre: ",padre)
print("Distancia: ",distancia)
print("\n\nTEST DIJKSTRA")

print("TEST DFS\n\n")
padre , orden = dfs(grafo,'a')
print("Padre: ",padre)
print("Orden: ",orden)
print("\n\nTEST DFS")

print("TEST BFS\n\n")
padre , orden = bfs(grafo,'a')
print("Padre: ",padre)
print("Orden: ",orden)
print("\n\nTEST BFS")

print(grafo)

grafo.sacar_vertice('c')
print(grafo)

grafo.agregar_arista('b','a',50)
print(grafo)

grafo.cambiar_peso('b','a',100)
print(grafo)

print(grafo.ver_aristas())


print("NUEVAS PRUEBAS GRAFO\n\n")

grafo1  = Grafo()
grafo1.agregar_vertice("0")
grafo1.agregar_vertice("1")
grafo1.agregar_vertice("2")
grafo1.agregar_vertice("3")
grafo1.agregar_vertice("4")
grafo1.agregar_vertice("5")
grafo1.agregar_vertice("6")
grafo1.agregar_vertice("7")
grafo1.agregar_arista("0","1",0)
grafo1.agregar_arista("1","2",0)
grafo1.agregar_arista("1","5",0)
grafo1.agregar_arista("2","3",0)
grafo1.agregar_arista("6","5",0)
grafo1.agregar_arista("6","7",0)
grafo1.agregar_arista("7","4",0)
grafo1.agregar_arista("4","3",0)
grafo1.agregar_arista("4","5",0)

print(grafo1)

print("PRUEBA BFS\n\n")

padre1,orden1 = bfs(grafo1,"1")

print(padre1)
print(orden1)

print("PRUEBA Dijkstra\n\n")

grafo2 = Grafo()

grafo2.agregar_vertice("A")
grafo2.agregar_vertice("B")
grafo2.agregar_vertice("C")
grafo2.agregar_vertice("D")
grafo2.agregar_vertice("E")
grafo2.agregar_vertice("F")
grafo2.agregar_vertice("G")
grafo2.agregar_arista("A","D",2)
grafo2.agregar_arista("D","C",8)
grafo2.agregar_arista("E","C",5)
grafo2.agregar_arista("D","E",2)
grafo2.agregar_arista("G","E",9)
grafo2.agregar_arista("B","D",4)
grafo2.agregar_arista("B","E",1)
grafo2.agregar_arista("B","G",5)
grafo2.agregar_arista("B","F",2)
grafo2.agregar_arista("A","G",1)
grafo2.agregar_arista("A","F",7)
grafo2.agregar_vertice("H")

print(grafo2.ver_adyacencia("C","D"))
print(grafo2.ver_a_adyacentes("H"))
v = grafo2.vertice_aleatorio()
print(grafo2.ver_aristas())

grafo3 = Grafo()
grafo3.agregar_vertice("a")
grafo3.agregar_vertice("b")
grafo3.agregar_vertice("c")
grafo3.agregar_vertice("d")
grafo3.agregar_vertice("e")
grafo3.agregar_vertice("f")
grafo3.agregar_vertice("g")
grafo3.agregar_arista("a","b",1)
grafo3.agregar_arista("a","c",5)
grafo3.agregar_arista("b","c",4)
grafo3.agregar_arista("d","c",6)
grafo3.agregar_arista("d","b",8)
grafo3.agregar_arista("d","e",11)
grafo3.agregar_arista("d","f",9)
grafo3.agregar_arista("b","e",7)
grafo3.agregar_arista("c","f",2)
grafo3.agregar_arista("e","f",2)
grafo3.agregar_arista("f","g",12)
grafo3.agregar_arista("e","g",10)

print("Prueba kruskaln\n\n")




grafo4 = Grafo()
grafo4.agregar_vertice("A")
grafo4.agregar_vertice("B")
grafo4.agregar_vertice("C")
grafo4.agregar_vertice("D")
grafo4.agregar_vertice("E")
grafo4.agregar_vertice("F")
grafo4.agregar_arista("A","B",2)
grafo4.agregar_arista("A","D",5)
grafo4.agregar_arista("A","C",1)
grafo4.agregar_arista("B","E",10)
grafo4.agregar_arista("B","D",1)
grafo4.agregar_arista("D","C",3)
grafo4.agregar_arista("C","F",7)
grafo4.agregar_arista("D","E",2)
grafo4.agregar_arista("F","E",6)




grafo5 = Grafo()
grafo5.agregar_vertice("A")
grafo5.agregar_vertice("B")
grafo5.agregar_vertice("C")
grafo5.agregar_vertice("D")
grafo5.agregar_vertice("E")
grafo5.agregar_arista("A","B",1)
grafo5.agregar_arista("B","E",1)
grafo5.agregar_arista("C","E",1)
grafo5.agregar_arista("A","C",1)
grafo5.agregar_arista("D","A",1)
grafo5.agregar_arista("D","B",2)
grafo5.agregar_arista("D","C",3)
grafo5.agregar_arista("D","E",4)

arbol5 = prim(grafo5)

print(arbol5)

print(arbol5.ver_aristas())

grafo6 = Grafo()

grafo6.agregar_vertice("A")
grafo6.agregar_vertice("B")
grafo6.agregar_vertice("C")
grafo6.agregar_vertice("D")
grafo6.agregar_vertice("E")
grafo6.agregar_vertice("F")
grafo6.agregar_vertice("G")
grafo6.agregar_arista("A","B",1)
grafo6.agregar_arista("A","C",5)
grafo6.agregar_arista("B","C",4)
grafo6.agregar_arista("B","E",7)
grafo6.agregar_arista("C","F",2)
grafo6.agregar_arista("E","F",3)
grafo6.agregar_arista("B","D",8)
grafo6.agregar_arista("E","D",11)
grafo6.agregar_arista("C","D",6)
grafo6.agregar_arista("F","D",9)
grafo6.agregar_arista("E","G",10)
grafo6.agregar_arista("F","G",12)

arbol6 = prim(grafo6)

print(arbol6.ver_aristas())

a = pesos_ady(grafo6,"D")
print(a)
print(vertice_aleatorio(a))

centralidad = centralidad_aproximada(grafo6,10,500)

print("Centralidad:",centralidad,"\n")


grafo7 = Grafo()
grafo7.agregar_vertice("A")
grafo7.agregar_vertice("B")
grafo7.agregar_vertice("C")
grafo7.agregar_vertice("D")
grafo7.agregar_vertice("E")
grafo7.agregar_vertice("F")
grafo7.agregar_arista("A","B",2)
grafo7.agregar_arista("A","C",1)
grafo7.agregar_arista("B","D",1)
grafo7.agregar_arista("C","D",3)
grafo7.agregar_arista("C","F",7)
grafo7.agregar_arista("F","E",6)
grafo7.agregar_arista("E","D",2)

prim1 = prim(grafo7)

print(prim1.ver_aristas())

centralidad = centralidad_aproximada(grafo7,10,100)

print("Centralidad aprox:",centralidad,"\n")

betw_centralidad = centralidad_betweeness(grafo7)

print("Super centralidad:",betw_centralidad,"\n")

print("Grafo usado:",str(grafo7),"\n")

grafo8 = Grafo()
grafo8.agregar_vertice("A")
grafo8.agregar_vertice("B")
grafo8.agregar_vertice("C")
grafo8.agregar_vertice("D")
grafo8.agregar_vertice("E")
grafo8.agregar_vertice("F")
grafo8.agregar_vertice("G")
grafo8.agregar_arista("A","B",1)
grafo8.agregar_arista("B","C",1)
grafo8.agregar_arista("B","D",1)
grafo8.agregar_arista("A","D",1)
grafo8.agregar_arista("A","E",1)
grafo8.agregar_arista("D","F",1)
grafo8.agregar_arista("D","E",1)
grafo8.agregar_arista("F","G",1)
grafo8.agregar_arista("E","G",1)

print("Grafo usado:",str(grafo8),"\n")

print("Los ady a 'A' son: ",grafo8.ver_a_adyacentes("A"))

print("Vacaciones con n = 0:",vacaciones(grafo8,'A',0),'\n')
print("Vacaciones con n = 1:",vacaciones(grafo8,'A',1),'\n')
print("Vacaciones con n = 2:",vacaciones(grafo8,'A',2),'\n')
print("Vacaciones con n = 3:",vacaciones(grafo8,'A',3),'\n')
print("Vacaciones con n = 4:",vacaciones(grafo8,'A',4),'\n')
print("Vacaciones con n = 5:",vacaciones(grafo8,'A',5),'\n')
print("Vacaciones con n = 6:",vacaciones(grafo8,'A',6),'\n')

grafo8.agregar_vertice("H")
grafo8.agregar_vertice("I")
grafo8.agregar_vertice("J")
grafo8.agregar_vertice("K")
grafo8.agregar_vertice("L")
grafo8.agregar_vertice("M")
grafo8.agregar_arista("E","H",1)
grafo8.agregar_arista("I","H",1)
grafo8.agregar_arista("I","J",1)
grafo8.agregar_arista("K","J",1)
grafo8.agregar_arista("K","L",1)
grafo8.agregar_arista("M","L",1)
grafo8.agregar_arista("M","G",1)

print("Vacaciones con n = 9:",vacaciones(grafo8,'A',9),'\n')
print("Vacaciones con n = 10:",vacaciones(grafo8,'A',10),'\n')
print("Vacaciones con n = 11:",vacaciones(grafo8,'A',11),'\n')

grafo8.agregar_vertice("Z")
grafo8.agregar_arista("A","Z",1)
grafo8.agregar_arista("Z","G",1)

print("Vacaciones con n = 9:",vacaciones(grafo8,'A',9),'\n')

print("Test greedy recorrer mundo aprox\n")

grafo9 = Grafo()
grafo9.agregar_vertice("A")
grafo9.agregar_vertice("B")
grafo9.agregar_vertice("C")
grafo9.agregar_vertice("D")
grafo9.agregar_vertice("E")
grafo9.agregar_vertice("F")
grafo9.agregar_vertice("G")
grafo9.agregar_arista("A","B",1)
grafo9.agregar_arista("B","D",1)
grafo9.agregar_arista("A","D",99)
grafo9.agregar_arista("A","E",1)
grafo9.agregar_arista("C","B",95)
grafo9.agregar_arista("D","F",1)
grafo9.agregar_arista("D","E",99)
grafo9.agregar_arista("F","G",1)
grafo9.agregar_arista("E","G",1)

print(global_greedy(grafo9,'A'))

print("Test greedy recorrer mundo aprox\n")

grafo10 = Grafo()

grafo10.agregar_vertice("A")
grafo10.agregar_vertice("B")
grafo10.agregar_vertice("C")
grafo10.agregar_vertice("D")
grafo10.agregar_vertice("E")
grafo10.agregar_vertice("F")
grafo10.agregar_vertice("G")
grafo10.agregar_arista("A","B",1)
grafo10.agregar_arista("A","C",5)
grafo10.agregar_arista("B","C",4)
grafo10.agregar_arista("B","E",7)
grafo10.agregar_arista("C","F",2)
grafo10.agregar_arista("E","F",3)
grafo10.agregar_arista("B","D",8)
grafo10.agregar_arista("E","D",11)
grafo10.agregar_arista("C","D",6)
grafo10.agregar_arista("F","D",9)
grafo10.agregar_arista("E","G",10)
grafo10.agregar_arista("F","G",12)


cent_b=centralidad_betweeness(grafo10)

print(cent_b)






