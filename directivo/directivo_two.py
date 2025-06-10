import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

def directivo_clases_horarios_por_modulo_dos():
    auth = HTTPBasicAuth("12344321", "DevUser123")

    # --- Descargas de datos ---
    url_modulos  = "https://cesde-academic-app-development.up.railway.app/modulo/lista"
    url_clases   = "https://cesde-academic-app-development.up.railway.app/clase/lista"
    url_horarios = "https://cesde-academic-app-development.up.railway.app/clase-horario/lista"

    df_mod     = pd.DataFrame(requests.get(url_modulos,  auth=auth).json())
    df_clases  = pd.DataFrame(requests.get(url_clases,  auth=auth).json())
    df_hor     = pd.DataFrame(requests.get(url_horarios, auth=auth).json())

    # --- Conteo de clases por módulo (nombre) ---
    clases_por_mod = (
        df_clases.groupby("modulo")
        .size()
        .reset_index(name="cantidad_de_clases_por_modulo")
    )

    # --- Conteo de horarios por módulo (en df_horarios 'clase' ya es nombre de módulo) ---
    horarios_por_mod = (
        df_hor.groupby("clase")
        .size()
        .reset_index(name="cantidad_de_horarios_por_modulo")
        .rename(columns={"clase": "modulo"})
    )

    # --- Unir ambos conteos ---
    comparativo = clases_por_mod.merge(
        horarios_por_mod,
        on="modulo",
        how="left"          # módulos sin horarios quedarán con NaN
    ).fillna(0)

    # Asegurar tipos correctos para JSON
    comparativo["modulo"] = comparativo["modulo"].astype(str)
    comparativo["cantidad_de_horarios_por_modulo"] = comparativo["cantidad_de_horarios_por_modulo"].astype(int)

    return comparativo.to_dict(orient="records")
