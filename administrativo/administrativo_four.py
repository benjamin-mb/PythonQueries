import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

def administrativo_conteo_horarios_por_dia_four():
   
    auth = HTTPBasicAuth("12344321", "DevUser123")

    # Descargar los horarios de todas las clases
    url = "https://cesde-academic-app-development.up.railway.app/clase-horario/lista"
    df_horarios = pd.DataFrame(requests.get(url, auth=auth).json())

    if df_horarios.empty or "dia" not in df_horarios.columns:
        return {"error": "No se encontraron horarios o falta la columna 'dia'"}

    # Orden de días según la API
    orden_dias = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO", "DOMINGO"]

    # Conteo por día, asegurando incluir días sin clases
    conteo = (
        df_horarios.groupby("dia").size()
        .reindex(orden_dias, fill_value=0)
        .reset_index(name="total")
        .rename(columns={"dia": "dia"})
    )

    return conteo.to_dict(orient="records")
