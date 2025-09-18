#!/usr/bin/env python3
"""CLI para ejecutar el flujo completo:
leer Excel de accidentes -> calcular indicador -> asignar a nodos -> calcular ruta

Ejemplo:
  PYTHONPATH=. python3 GrafosYDosRuedas/cli.py --accidentes data/os2_sin_2025_08.xlsx \
    --agrupar COMUNA --inicio 1 --objetivo 3 --alg astar --w_dist 1.0 --w_elev 0.01 --w_seg 1.0
"""

import argparse
import json
import os

from classes.grafo import Grafo
from classes import routing
from classes import safety
from classes.utils import guardar_grafo_json


def construir_grafo_de_ejemplo():
    # Ejemplo mínimo; en producción deberías construir el grafo desde OSM o shapefiles
    g = Grafo()
    g.agregar_nodo(1, -33.45, -70.65, 0.0, 0.0)
    g.agregar_nodo(2, -33.46, -70.66, 0.0, 0.0)
    g.agregar_nodo(3, -33.47, -70.67, 0.0, 0.0)
    g.agregar_camino(101, 1, 2, ciclovia=True, importancia=2)
    g.agregar_camino(102, 2, 3, ciclovia=False, importancia=3)
    return g


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--accidentes', help='Ruta al Excel de accidentes', required=True)
    p.add_argument('--agrupar', help='Columna para agrupar (ej: COMUNA, ZONA)', default='COMUNA')
    p.add_argument('--inicio', type=int, help='ID nodo inicio', required=True)
    p.add_argument('--objetivo', type=int, help='ID nodo objetivo', required=True)
    p.add_argument('--alg', choices=['astar', 'dijkstra'], default='astar')
    p.add_argument('--w_dist', type=float, default=1.0)
    p.add_argument('--w_elev', type=float, default=0.0)
    p.add_argument('--w_seg', type=float, default=1.0)
    p.add_argument('--out_dir', default='.')

    args = p.parse_args()

    # construir o cargar grafo
    g = construir_grafo_de_ejemplo()

    # calcular indicador de seguridad
    print(f'Calculando indicador desde {args.accidentes} agrupando por {args.agrupar}...')
    scores = safety.calcular_indicador_seguridad_desde_excel(args.accidentes, agrupar_por=args.agrupar)
    norm = safety.normalizar_scores(scores)
    print(f'Grupos calculados: {len(norm)}')

    # Nota: este ejemplo espera que los nodos tengan atributo `comuna` o similar.
    # En la práctica debes asignar `nodo.comuna` cuando importes/crees nodos.
    print('Asignando indicador a nodos... (buscando atributo "comuna")')
    routing.asignar_indicador_seguridad(g, norm, nodo_attr='comuna')

    # calcular ruta
    if args.alg == 'astar':
        ruta = routing.a_estrella(g, args.inicio, args.objetivo, w_dist=args.w_dist, w_elev=args.w_elev, w_seg=args.w_seg)
    else:
        _, prev = routing.dijkstra(g, args.inicio, goal_id=args.objetivo, w_dist=args.w_dist, w_elev=args.w_elev, w_seg=args.w_seg)
        ruta = routing.reconstruir_camino(prev, args.inicio, args.objetivo)

    print('Ruta calculada:', ruta)

    os.makedirs(args.out_dir, exist_ok=True)
    ruta_file = os.path.join(args.out_dir, 'ruta_cli.json')
    with open(ruta_file, 'w', encoding='utf-8') as f:
        json.dump({'ruta': ruta}, f, ensure_ascii=False, indent=2)
    print('Ruta guardada en', ruta_file)

    # guardar grafo
    guardar_grafo_json(g, os.path.join(args.out_dir, 'grafo_cli.json'))


if __name__ == '__main__':
    main()
