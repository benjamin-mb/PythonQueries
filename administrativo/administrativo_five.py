import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

def administrativo_promedio_notas_por_clase_five():
    
    auth = HTTPBasicAuth("12344321", "DevUser123")

    # --- Descargar datos ---
    df_clases = pd.DataFrame(requests.get(
        "https://cesde-academic-app-development.up.railway.app/clase/lista", auth=auth).json())

    df_calif  = pd.DataFrame(requests.get(
        "https://cesde-academic-app-development.up.railway.app/calificacion/lista", auth=auth).json())

    df_activ  = pd.DataFrame(requests.get(
        "https://cesde-academic-app-development.up.railway.app/actividad/lista", auth=auth).json())

    if df_clases.empty or df_calif.empty:
        return {"error": "No se encontraron datos de clases o calificaciones"}

    # --- Preparar actividades para poder unir por 'actividad' y 'fecha' ---
    df_activ = df_activ.rename(columns={"tipo": "actividad", "fechaEntrega": "fecha"})

    # --- Unir calificaciones con actividades (para validar actividad/fecha) ---
    df_notas = df_calif.merge(df_activ, on=["actividad", "fecha"], how="left")

    # --- Extraer 'grupo' del campo anidado 'clase' ---
    if "clase" in df_notas.columns:
        df_notas["grupo"] = df_notas["clase"].apply(lambda c: c.get("grupo") if isinstance(c, dict) else None)
    else:
        df_notas["grupo"] = None  # fallback

    # --- Unir con df_clases para obtener id de clase, módulo, docente ---
    df_notas = df_notas.merge(df_clases, on="grupo", how="left", suffixes=('', '_clase'))

    # --- Calcular promedio por clase id ---
    df_prom = (
        df_notas.groupby("id")["nota"]
        .mean()
        .reset_index(name="promedio_nota")
        .merge(
            df_clases[["id", "grupo", "modulo", "docente"]],
            on="id",
            how="left"
        )
        .rename(columns={"id": "clase_id"})
        .sort_values(by="promedio_nota", ascending=False)
    )

    return df_prom.to_dict(orient="records")
