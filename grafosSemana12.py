laboratorios = {
    "Redes": {"Software"},
    "Software": {"Datos", "Robotica"},
    "Robotica": {"Electronica"},
    "Datos": {"Electronica"},
    "Seguridad": {"Redes"}

}

def showConections(laboratorios):
    for vertice, vecinos in laboratorios.items():
        print(vertice, "->", vecinos)
showConections(laboratorios)

def consultarVecinos(laboratorios, vertice):
    if vertice not in laboratorios:
        return None
    return laboratorios[vertice]
print("Conexiones SOFTWARE: ", consultarVecinos(laboratorios, "Software"))

def countConections(laboratorios, vertice):
    if vertice in laboratorios:
        return len(laboratorios[vertice])
    return 0 

print("Numero de conecciones: ", countConections(laboratorios, "Software"))

