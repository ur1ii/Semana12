"""Módulo del grafo: lista de adyacencia, BFS y DFS.

El grafo es NO dirigido: una conexión A-B se puede recorrer en ambos sentidos.
Los vértices representan edificios del campus.
"""
from collections import deque


class Grafo:
    def __init__(self):
        # Lista de adyacencia: {vertice: [vecinos...]}
        self.adyacencia = {}

    def agregar_vertice(self, vertice):
        """Agrega un vértice si no existe todavía."""
        self.adyacencia.setdefault(vertice, [])

    def agregar_arista(self, a, b):
        """Conecta a y b (crea los vértices si faltan). Evita duplicados."""
        self.agregar_vertice(a)
        self.agregar_vertice(b)
        if b not in self.adyacencia[a]:
            self.adyacencia[a].append(b)
        if a not in self.adyacencia[b]:
            self.adyacencia[b].append(a)

    def existe(self, vertice):
        return vertice in self.adyacencia

    def a_dict(self):
        """Devuelve la lista de adyacencia con vecinos ordenados."""
        return {v: sorted(vs) for v, vs in sorted(self.adyacencia.items())}

    def bfs_ruta(self, origen, destino):
        """Ruta con MENOS aristas entre origen y destino usando BFS.

        Usa una cola (FIFO) y un diccionario `padre` para reconstruir el
        camino. Devuelve una lista de vértices o None si no hay ruta.
        """
        if origen == destino:
            return [origen]
        padre = {origen: None}
        cola = deque([origen])
        while cola:
            actual = cola.popleft()
            for vecino in sorted(self.adyacencia[actual]):
                if vecino not in padre:
                    padre[vecino] = actual
                    if vecino == destino:
                        ruta = []
                        while vecino is not None:
                            ruta.append(vecino)
                            vecino = padre[vecino]
                        return ruta[::-1]
                    cola.append(vecino)
        return None

    def dfs(self, inicio):
        """Recorrido DFS iterativo (pila) desde `inicio`.

        Devuelve los vértices alcanzables en el orden en que se visitan.
        """
        visitados, orden = set(), []
        pila = [inicio]
        while pila:
            actual = pila.pop()
            if actual in visitados:
                continue
            visitados.add(actual)
            orden.append(actual)
            # Se apilan en orden inverso para visitar primero el menor
            for vecino in sorted(self.adyacencia[actual], reverse=True):
                if vecino not in visitados:
                    pila.append(vecino)
        return orden