import requests

def obtener_coordenadas_osm(direccion: str):
    url = "https://photon.komoot.io/api/"

    params = {
        "q": f"{direccion}, Región Metropolitana, Chile",
        "limit": 1
    }

    headers = {
        "User-Agent": "MiAppGeolocalizacion/1.0"
    }

    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        if r.status_code != 200:
            print("Error HTTP:", r.status_code)
            print("Respuesta:", r.text[:200])
            return None

        data = r.json()

        features = data.get("features", [])
        if not features:
            print("Dirección no encontrada.")
            return None

        coords = features[0]["geometry"]["coordinates"]
        lon, lat = coords
        return lat, lon

    except Exception as e:
        print("Error:", e)
        return None


# Prueba
print(obtener_coordenadas_osm("cenco ñuñoa"))
