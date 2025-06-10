import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

def administrativo_distribucion_estudiantes_por_programa_one():
    
    auth = HTTPBasicAuth("12344321", "DevUser123")

    # --- Descarga de datos ---
    urls = {
        "grupos": "https://cesde-academic-app-development.up.railway.app/grupo/lista",
        "grupo_estudiante": "https://cesde-academic-app-development.up.railway.app/grupo-estudiante/lista"
    }

    df_grupos = pd.DataFrame(requests.get(urls["grupos"], auth=auth).json())
    df_grupo_est = pd.DataFrame(requests.get(urls["grupo_estudiante"], auth=auth).json())

    if df_grupos.empty or df_grupo_est.empty:
        return {"error": "No se pudieron obtener datos de grupos o estudiantes"}

    # --- Total de estudiantes por grupo ---
    estudiantes_por_grupo = (
        df_grupo_est.groupby("grupoId")
        .size()
        .reset_index(name="total_estudiantes")
    )

    # --- Añadir nombre del programa a cada grupo ---
    grupos_info = df_grupos[["id", "programa"]].rename(columns={"id": "grupoId"})

    estudiantes_con_programa = estudiantes_por_grupo.merge(
        grupos_info,
        on="grupoId",
        how="left"
    )

    # --- Sumar estudiantes para cada programa ---
    distribucion = (
        estudiantes_con_programa.groupby("programa")["total_estudiantes"]
        .sum()
        .reset_index()
        .sort_values(by="total_estudiantes", ascending=False)
    )

    return distribucion.to_dict(orient="records")
