from typing import List, Optional
from .camino import Camino

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
        self.caminos: List[Camino] = []
        self.vecinos: List['Nodo'] = []

    def agregar_camino(self, camino: Camino):
        if camino not in self.caminos:
            self.caminos.append(camino)
            otro = camino.obtener_otro_nodo(self)
            if otro and otro not in self.vecinos:
                self.vecinos.append(otro)

    def __repr__(self):
        return f"Nodo({self.id}, lat={self.latitud}, lon={self.longitud}, alt={self.altura}, p_acc={self.prob_accidente})"
