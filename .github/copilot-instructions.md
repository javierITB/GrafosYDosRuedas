## Purpose
This file gives focused, actionable guidance for AI coding agents working on this repository (GrafosYDosRuedas).

## Quick tasks & commands
- Run unit tests (from repo root):
  - `PYTHONPATH=. python3 -m unittest discover -s GrafosYDosRuedas/tests -v`
- Run the example script:
  - `PYTHONPATH=. python3 GrafosYDosRuedas/main.py`
- Run CLI end-to-end (builds graph from OSM, computes safety indicator and route):
  - `PYTHONPATH=. python3 GrafosYDosRuedas/cli.py --accidentes <xlsx> --agrupar COMUNA --inicio <id> --objetivo <id> --alg astar`

## High-level architecture (what to look at)
- `classes/` is the core package. Key modules:
  - `nodo.py` — node model; dynamic attributes (e.g. `comuna`) are commonly attached at runtime.
  - `camino.py` — edge model connecting two `Nodo` instances.
  - `grafo.py` — container for nodes and edges; simple dict-backed storage.
  - `routing.py` — algorithms: `dijkstra`, `a_estrella` (A*), cost function `coste_arista`, and helper `distancia_haversine`.
  - `safety.py` — computes safety indicator from Excel (uses `pandas`) and `normalizar_scores`.
  - `utils.py` / `utils2.py` — JSON export and optional elevation estimation.

## Data flow and common flows
- OSM -> graph: `cli.construir_grafo_desde_osm()` parses `data/map_with_elevation.osm` and calls `Grafo.agregar_nodo` / `agregar_camino`.
- Accidents Excel -> safety scores: `safety.calcular_indicador_seguridad_desde_excel(...)` -> `safety.normalizar_scores(...)`.
- Assigning safety to nodes: `routing.asignar_indicador_seguridad(grafo, scores, nodo_attr='comuna')` expects nodes to have the grouping attribute (often `comuna`).
- Routing: call `routing.a_estrella` or `routing.dijkstra` with weights `w_dist`, `w_elev`, `w_seg`. Output routes are lists of node IDs and commonly written to `ruta_cli.json` or `ruta_ejemplo_*.json`.

## Project-specific conventions and gotchas
- Language & names: code uses Spanish identifiers and comments — search for `comuna`, `prob_accidente`, `importancia` rather than English names.
- Dynamic node attributes: code often sets attributes like `nodo.comuna` after node creation; do not assume all attributes exist — use `hasattr` where appropriate.
- Weights and safety semantics:
  - `routing.coste_arista` composes three components: distance (meters), positive elevation gain, and safety penalty computed as `nodo_destino.prob_accidente * (1.0 / max(1.0, camino.importancia))`.
  - Larger `camino.importancia` reduces the safety penalty because cost uses `1.0 / importancia`.
  - A* heuristic is intentionally admissible: it uses only geographic distance scaled by `w_dist`. Avoid changing this to include non-admissible terms unless you adjust correctness proofs/tests.
- Lazy imports: code often imports heavy deps (like `pandas`) inside functions to keep module import light. Follow this pattern for optional heavy dependencies.

## Integration points & external dependencies
- `pandas` is required to run `safety.calcular_indicador_seguridad_desde_excel` and related tests. Tests skip if pandas is not installed.
- OSM input file: `data/map_with_elevation.osm` is the default for CLI graph construction.
- JSON outputs used by tools/tests: `grafo.json`, `grafo_cli.json`, `ruta_cli.json`, `ruta_ejemplo_ast.json`, `ruta_ejemplo_dijkstra.json`.

## Testing and change-sensitivity
- Tests live in `GrafosYDosRuedas/tests/` and include focused unit tests for routing and safety.
- When changing routing cost semantics (`coste_arista`) or `asignar_indicador_seguridad`, update these tests and the small example in `main.py`/`cli.py`.

## Files to inspect when editing behaviors
- Routing: `classes/routing.py` (heuristic, cost composition, aliases for retrocompatibility such as `astar`)
- Safety: `classes/safety.py` (score formula, normalization)
- IO & Helpers: `classes/utils.py`, `classes/utils2.py`, `Extractor.py` (Excel -> graph mapping)
- CLI & examples: `cli.py`, `main.py`

## Minimal rules for AI edits
- Preserve external-facing function signatures (e.g. `dijkstra(..., goal_id=...)` compatibility) to avoid breaking CLI/tests.
- Keep A* heuristic admissible (distance-only) unless you run and update tests proving no regressions.
- When adding dependencies (pandas, geopandas, numpy), add them to `requirements.txt` and keep imports local if only used in specific functions.

## Example snippets (copy-paste safe)
- Call A* with safety and elevation weights:
  - `routing.a_estrella(g, inicio_id, objetivo_id, w_dist=1.0, w_elev=0.01, w_seg=1.0)`
- Assign safety scores after computing them from an Excel file:
  - `scores = safety.normalizar_scores(safety.calcular_indicador_seguridad_desde_excel('data/os.xlsx', agrupar_por='COMUNA'))`
  - `routing.asignar_indicador_seguridad(g, scores, nodo_attr='comuna')`

If anything here is unclear or you'd like a different level of detail (more examples, docstrings to update, or automated checks), tell me which sections to expand and I'll iterate.
