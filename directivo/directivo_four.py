import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

def directivo_escuela_mas_programas_four():
   
    auth = HTTPBasicAuth("12344321", "DevUser123")

    # Obtener programas
    url_programas = "https://cesde-academic-app-development.up.railway.app/programa/lista"
    df_programas = pd.DataFrame(requests.get(url_programas, auth=auth).json())

    if df_programas.empty or "escuela" not in df_programas.columns:
        return {"error": "No se encontraron programas o columna 'escuela' ausente"}

    # Conteo de programas por escuela
    conteo = (
        df_programas.groupby("escuela")
        .size()
        .reset_index(name="cantidad_programas")
    )

    # Valor máximo
    max_programas = conteo["cantidad_programas"].max()

    # Escuelas con el máximo
    top_escuelas = conteo[conteo["cantidad_programas"] == max_programas]

    return top_escuelas.to_dict(orient="records")
