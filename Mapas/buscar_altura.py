import pandas as pd
import numpy as np
from scipy.spatial import cKDTree

# Cargar el dataset
df = pd.read_csv("alturas_santiago.csv")  # reemplaza con tu archivo CSV

# Crear un árbol para búsqueda rápida de vecinos
coords = df[['lat', 'lon']].values
tree = cKDTree(coords)

def altura_aproximada(lat, lon, k=3):
    """
    Estima la altura (ele) de un punto (lat, lon)
    usando interpolación promedio de los k vecinos más cercanos.
    """
    # Buscar los k vecinos más cercanos
    distancias, indices = tree.query([lat, lon], k=k)
    
    # Obtener sus alturas
    alturas = df.iloc[indices]['ele'].values
    
    # Retornar la altura promedio ponderada por la distancia
    if k == 1:
        return alturas[0]
    else:
        # Evitar división por cero
        pesos = 1 / (distancias + 1e-8)
        altura_estimada = np.sum(pesos * alturas) / np.sum(pesos)
        return altura_estimada

# Ejemplo de uso
lat_test = -33.394459675
lon_test = -70.621984918
altura = altura_aproximada(lat_test, lon_test)
print(f"Altura aproximada: {altura:.2f} m")
