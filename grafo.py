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

import random

                    ########################
                    #                      #
                    #        CLASES        #
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
