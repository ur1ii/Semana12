grafo = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A", "D", "E"],
    "D": ["B", "C", "F"],
    "E": ["C", "F"],
    "F": ["D", "E"],
}

def mostrar_vecinos(grafo, vertice):
    if vertice not in grafo:
        return []
    return grafo[vertice]

print(mostrar_vecinos(grafo, "C"))


def contar_vertices(grafo):
    if not grafo:
        return None
    total = len(grafo)
    return total
    
print(contar_vertices(grafo))

def contar_aristas(grafo):
    if not grafo:
        return None
    suma = 0
    for aristas in grafo:
        total = len(grafo[aristas])
        suma += total
    aristas = suma / 2
    return aristas

print(contar_aristas(grafo))

    

