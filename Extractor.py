from typing import List, Dict, Optional
import json

class Nodo:
    def __init__(self,
                 id_nodo: int,
                 latitud: float,
                 longitud: float,
                 altura: float = 0.0,
                 prob_accidente: float = 0.0):
        self.id = id_nodo
        self.latitud = latitud
        self.longitud = longitud
        self.altura = altura
        self.prob_accidente = prob_accidente
        self.caminos: List['Camino'] = []       # Caminos que pasan por este nodo
        self.vecinos: List['Nodo'] = []         # Nodos conectados

    def agregar_camino(self, camino: 'Camino'):
        if camino not in self.caminos:
            self.caminos.append(camino)
            # Asegurar consistencia: agregar nodo vecino
            otro = camino.obtener_otro_nodo(self)
            if otro and otro not in self.vecinos:
                self.vecinos.append(otro)

    def __repr__(self):
        return f"Nodo({self.id}, lat={self.latitud}, lon={self.longitud}, alt={self.altura}, p_acc={self.prob_accidente})"


class Camino:
    def __init__(self,
                 id_camino: int,
                 nodo_a: Nodo,
                 nodo_b: Nodo,
                 ciclovia: bool = False,
                 importancia: int = 1):
        self.id = id_camino
        self.nodos = (nodo_a, nodo_b)       # conexión entre nodos
        self.ciclovia = ciclovia
        self.importancia = importancia
        self.vecinos: List['Camino'] = []   # Caminos que comparten nodo

        # Enlazar a nodos
        nodo_a.agregar_camino(self)
        nodo_b.agregar_camino(self)

    def agregar_vecino(self, otro: 'Camino'):
        if otro not in self.vecinos and otro is not self:
            self.vecinos.append(otro)

    def obtener_otro_nodo(self, nodo: Nodo) -> Optional[Nodo]:
        """Dado un nodo, retorna el otro extremo del camino."""
        if nodo == self.nodos[0]:
            return self.nodos[1]
        elif nodo == self.nodos[1]:
            return self.nodos[0]
        return None

    def __repr__(self):
        return f"Camino({self.id}, nodos=({self.nodos[0].id}, {self.nodos[1].id}), ciclovia={self.ciclovia}, imp={self.importancia})"


class Grafo:
    def __init__(self):
        self.nodos: Dict[int, Nodo] = {}
        self.caminos: Dict[int, Camino] = {}

    def agregar_nodo(self, id_nodo: int, lat: float, lon: float, alt: float = 0.0, prob_acc: float = 0.0) -> Nodo:
        if id_nodo not in self.nodos:
            self.nodos[id_nodo] = Nodo(id_nodo, lat, lon, alt, prob_acc)
        return self.nodos[id_nodo]

    def agregar_camino(self, id_camino: int, id_nodo_a: int, id_nodo_b: int, ciclovia: bool = False, importancia: int = 1) -> Camino:
        if id_camino not in self.caminos:
            nodo_a = self.nodos[id_nodo_a]
            nodo_b = self.nodos[id_nodo_b]
            self.caminos[id_camino] = Camino(id_camino, nodo_a, nodo_b, ciclovia, importancia)
        return self.caminos[id_camino]

    def __repr__(self):
        return f"Grafo(nodos={len(self.nodos)}, caminos={len(self.caminos)})"


def guardar_grafo_json(grafo: Grafo, ruta_archivo: str):
    """
    Guarda el grafo en un archivo JSON con toda la información de nodos y caminos.
    """
    data = {
        "nodos": [],
        "caminos": []
    }

    # Guardar nodos
    for nodo in grafo.nodos.values():
        data["nodos"].append({
            "id": nodo.id,
            "latitud": nodo.latitud,
            "longitud": nodo.longitud,
            "altura": nodo.altura,
            "prob_accidente": nodo.prob_accidente,
            "vecinos": [v.id for v in nodo.vecinos],
            "caminos": [c.id for c in nodo.caminos]
        })

    # Guardar caminos
    for camino in grafo.caminos.values():
        data["caminos"].append({
            "id": camino.id,
            "nodos": [camino.nodos[0].id, camino.nodos[1].id],
            "ciclovia": camino.ciclovia,
            "importancia": camino.importancia,
            "vecinos": [c.id for c in camino.vecinos]
        })

    with open(ruta_archivo, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Grafo guardado en {ruta_archivo}")


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
