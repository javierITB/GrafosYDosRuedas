import unittest
import sys
import os

# Ensure package imports from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classes.grafo import Grafo
from classes import routing


class TestRouting(unittest.TestCase):
    def setUp(self):
        self.g = Grafo()
        self.g.agregar_nodo(1, -33.45, -70.65, 600, 0.1)
        self.g.agregar_nodo(2, -33.46, -70.66, 605, 0.05)
        self.g.agregar_nodo(3, -33.47, -70.67, 610, 0.2)
        self.g.agregar_camino(101, 1, 2, ciclovia=True, importancia=2)
        self.g.agregar_camino(102, 2, 3, ciclovia=False, importancia=3)

    def test_astar_basic(self):
        path = routing.a_estrella(self.g, 1, 3, w_dist=1.0, w_elev=0.01, w_seg=10.0)
        self.assertIsNotNone(path)
        self.assertEqual(path, [1, 2, 3])

    def test_dijkstra_distances(self):
        dist, prev = routing.dijkstra(self.g, 1, goal_id=3, w_dist=1.0, w_elev=0.0, w_seg=0.0)
        self.assertIn(3, dist)
        self.assertIsNotNone(prev[3])


if __name__ == '__main__':
    unittest.main()
