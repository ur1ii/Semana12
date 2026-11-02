grafo = {
    "Managua": ["León", "Granada", "Masaya"],
    "León": ["Managua", "Esteli"],
    "Granada": ["Managua", "Masaya"],
    "Masaya": ["Managua", "Granada"],
    "Esteli": ["Leon"],
}

def mostrar_grafo(conexiones):
    for vertice, vecinos in conexiones.items():
        print(vertice, "->", ", ".join(vecinos))


mostrar_grafo(grafo)

vertices = ["A", "B", "C", "D"]
matriz = [
    [0, 1, 1, 1],
    [1, 0, 1, 0],
    [1, 1, 0, 1],
    [1, 0, 1, 0]
]


def mostrar_matriz(nodos, conexiones):
    print("   ", " ".join(nodos))
    for i in range(len(nodos)):
        print(nodos[i], " ", " ".join(map(str, conexiones[i])))


mostrar_matriz(vertices, matriz)

def agregar_vertice(grafo, vertice):
    if vertice not in grafo:
        grafo[vertice] = []
        return True
    return False


def agregar_arista(grafo, origen, destino):
    if origen not in grafo or destino not in grafo:
        return False
    if origen == destino:
        return False
    if destino in grafo[origen]:
        return False

    grafo[origen].append(destino)
    grafo[destino].append(origen)
    return True


def consultar_vecinos(grafo, vertice):
    if vertice not in grafo:
        return None
    return grafo[vertice][:]


def existe_arista(grafo, origen, destino):
    return origen in grafo and destino in grafo[origen]


def mostrar_grafo(grafo):
    for vertice, vecinos in grafo.items():
        print(vertice, "->", vecinos)


grafo = {}
for ciudad in ["Managua", "León", "Granada", "Masaya"]:
    agregar_vertice(grafo, ciudad)

agregar_arista(grafo, "Managua", "León")
agregar_arista(grafo, "Managua", "Granada")
agregar_arista(grafo, "Masaya", "Granada")
mostrar_grafo(grafo)
print("Vecinos de Managua:", consultar_vecinos(grafo, "Managua"))
print("¿Conexión León-Granada?:", existe_arista(grafo, "León", "Granada"))
print("¿Conexión Masaya-Managua?:", existe_arista(grafo, "Masaya", "Managua"))

def eliminar_arista(grafo, origen, destino):
    if origen not in grafo or destino not in grafo:
        return False
    if destino not in grafo[origen]:
        return False

    grafo[origen].remove(destino)
    grafo[destino].remove(origen)
    return True


def eliminar_vertice(grafo, vertice):
    if vertice not in grafo:
        return False

    for vecino in grafo[vertice][:]:
        grafo[vecino].remove(vertice)
    del grafo[vertice]
    return True


grafo = {
    "A": ["B", "C"],
    "B": ["A", "C"],
    "C": ["A", "B"]
}

eliminar_arista(grafo, "B", "C")
print("Después de eliminar B-C:", grafo)
eliminar_vertice(grafo, "C")
print("Después de eliminar C:", grafo)

rutas = {
    "A": {"B": 12, "C": 20},
    "B": {"A": 12, "C": 7, "D": 9},
    "C": {"A": 20, "B": 7, "D": 4},
    "D": {"C": 4}
}

def costo_directo(grafo, origen, destino):
    if origen not in grafo:
        return None
    return grafo[origen].get(destino)


print("Costo A-C:", costo_directo(rutas, "A", "C"))
print("Costo A-D:", costo_directo(rutas, "A", "D"))
print("Costo B-D:", costo_directo(rutas, "B", "D"))
print("Costo C-D:", costo_directo(rutas, "C", "D"))
print("Costo de A-B-C:", costo_directo(rutas, "A", "B") +
      costo_directo(rutas, "B", "C"))
print("Costo de A-C-D:", costo_directo(rutas, "A", "C") +
      costo_directo(rutas, "C", "D"))