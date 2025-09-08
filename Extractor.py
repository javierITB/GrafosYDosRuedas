from typing import List, Dict, Optional

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
