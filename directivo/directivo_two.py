import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

def directivo_clases_horarios_por_modulo_dos():
    auth = HTTPBasicAuth("12344321", "DevUser123")

    # --- Descargas ---
    url_modulos = "https://cesde-academic-app-development.up.railway.app/modulo/lista"
    url_clases = "https://cesde-academic-app-development.up.railway.app/clase/lista"
    url_horarios = "https://cesde-academic-app-development.up.railway.app/clase-horario/lista"

    df_modulos = pd.DataFrame(requests.get(url_modulos,  auth=auth).json())
    df_clases  = pd.DataFrame(requests.get(url_clases,  auth=auth).json())
    df_hor     = pd.DataFrame(requests.get(url_horarios, auth=auth).json())

    # --- nº de clases por módulo ---
    clases_por_mod = (
        df_clases.groupby("modulo").size()
        .reset_index(name="cantidad_de_clases_por_modulo")
    )

    # --- nº de horarios por clase ---
    hor_por_clase = (
        df_hor.groupby("clase").size()
        .reset_index(name="cantidad_de_horarios_por_clase")
    )

    # Alineamos tipos para poder unir
    hor_por_clase["clase"] = pd.to_numeric(hor_por_clase["clase"], errors="coerce").astype("Int64")
    df_clases["id"]        = pd.to_numeric(df_clases["id"],        errors="coerce").astype("Int64")

    # Vinculamos cada horario con el módulo de su clase
    hor_con_mod = hor_por_clase.merge(
        df_clases[["id", "modulo"]],
        left_on="clase",
        right_on="id",
        how="left"
    )

    # Sumamos horarios por módulo
    hor_por_mod = (
        hor_con_mod.groupby("modulo")["cantidad_de_horarios_por_clase"]
        .sum()
        .reset_index()
    )

    # --- Unimos ambos conteos ---
    comparativo = clases_por_mod.merge(
        hor_por_mod,
        on="modulo",
        how="outer"
    ).fillna(0)

    # Garantizar formato serializable
    comparativo["modulo"] = comparativo["modulo"].astype(str)

    return comparativo.to_dict(orient="records")
