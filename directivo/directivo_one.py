import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

def directivo_programas_por_escuela_uno():
    auth = HTTPBasicAuth("12344321", "DevUser123")

    url_programas = "https://cesde-academic-app-development.up.railway.app/programa/lista"
    response = requests.get(url_programas, auth=auth)
    if response.status_code != 200:
        return {"error": "No se pudieron obtener los programas"}

    data = response.json()
    df = pd.DataFrame(data)

    conteo = df.groupby("escuela").size().reset_index(name="cantidad_programas")
    resultado = conteo.to_dict(orient="records")

    return resultado
    