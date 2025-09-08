from classes.grafo import Grafo
from classes.utils import guardar_grafo_json, actualizar_alturas

if __name__ == "__main__":
    g = Grafo()

    # Crear nodos
    g.agregar_nodo(1, -33.45, -70.65, 600, 0.1)
    g.agregar_nodo(2, -33.46, -70.66, 605, 0.05)
    g.agregar_nodo(3, -33.47, -70.67, 610, 0.2)

    # Crear caminos
    g.agregar_camino(101, 1, 2, ciclovia=True, importancia=2)
    g.agregar_camino(102, 2, 3, ciclovia=False, importancia=3)

    # Mostrar grafo
    print(g)
    print(g.nodos[1])
    print(g.caminos[101])

    # Guardar en JSON
    guardar_grafo_json(g, "grafo.json")
