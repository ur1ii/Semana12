"""Servidor Flask: endpoints y validación de datos."""
from flask import Flask, jsonify, render_template, request
from grafo import Grafo

app = Flask(__name__)
grafo = Grafo()

# Datos de ejemplo (campus)
for a, b in [("Biblioteca", "Rectoría"), ("Biblioteca", "Cafetería"),
             ("Rectoría", "Auditorio"), ("Cafetería", "Laboratorio"),
             ("Auditorio", "Laboratorio")]:
    grafo.agregar_arista(a, b)
grafo.agregar_vertice("Gimnasio")  # edificio aislado: prueba "sin ruta"


def limpiar(valor):
    """Normaliza un texto: None -> '' y recorta espacios."""
    return (valor or "").strip()


def error(mensaje, codigo=400):
    return jsonify({"error": mensaje}), codigo


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/grafo")
def api_grafo():
    """Consulta la lista de adyacencia."""
    return jsonify({"adyacencia": grafo.a_dict()})


@app.post("/api/conexiones")
def api_conexiones():
    """Agrega una conexión {origen, destino}. Si solo se envía origen, crea el vértice."""
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        return error("Se esperaba un JSON válido.")
    origen, destino = limpiar(datos.get("origen")), limpiar(datos.get("destino"))
    if not origen:
        return error("El campo 'origen' es obligatorio.")
    if not destino:
        grafo.agregar_vertice(origen)
        return jsonify({"mensaje": f"Edificio '{origen}' agregado.",
                        "adyacencia": grafo.a_dict()}), 201
    if origen == destino:
        return error("Un edificio no puede conectarse consigo mismo.")
    grafo.agregar_arista(origen, destino)
    return jsonify({"mensaje": f"Conexión {origen} — {destino} agregada.",
                    "adyacencia": grafo.a_dict()}), 201


@app.get("/api/ruta")
def api_ruta():
    """Ruta más corta (en aristas) con BFS: /api/ruta?origen=A&destino=B"""
    origen = limpiar(request.args.get("origen"))
    destino = limpiar(request.args.get("destino"))
    if not origen or not destino:
        return error("Parámetros 'origen' y 'destino' obligatorios.")
    for nombre in (origen, destino):
        if not grafo.existe(nombre):
            return error(f"El edificio '{nombre}' no existe.", 404)
    ruta = grafo.bfs_ruta(origen, destino)
    if ruta is None:
        return jsonify({"existe": False, "ruta": [],
                        "mensaje": f"No existe ruta entre {origen} y {destino}."})
    return jsonify({"existe": True, "ruta": ruta, "pasos": len(ruta) - 1})


@app.get("/api/recorrido")
def api_recorrido():
    """Recorrido DFS: /api/recorrido?inicio=A"""
    inicio = limpiar(request.args.get("inicio"))
    if not inicio:
        return error("Parámetro 'inicio' obligatorio.")
    if not grafo.existe(inicio):
        return error(f"El edificio '{inicio}' no existe.", 404)
    return jsonify({"inicio": inicio, "recorrido": grafo.dfs(inicio)})


if __name__ == "__main__":
    app.run(debug=True)