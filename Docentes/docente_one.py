import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

#Cuál es el promedio de notas de mis estudiantes por asignatura?

def docente_promedios_grupo_one():
    auth = HTTPBasicAuth("12344321", "DevUser123")
    codigo_grupo = "P1-S2025-1-1"

    # 1. Obtener ID del grupo a partir del código
    url_grupo = f"https://cesde-academic-app-development.up.railway.app/grupo/buscar/codigo/{codigo_grupo}"
    response_grupo = requests.get(url_grupo)
    if response_grupo.status_code != 200 or not response_grupo.json():
        return {"error": f"No se encontró grupo con código {codigo_grupo}"}

    grupo_id = response_grupo.json()[0]['id']

    # 2. Obtener estudiantes del grupo
    url_estudiantes = f"https://cesde-academic-app-development.up.railway.app/grupo-estudiante/grupo/{grupo_id}"
    response_estudiantes = requests.get(url_estudiantes)
    if response_estudiantes.status_code != 200:
        return {"error": "No se pudieron obtener los estudiantes del grupo"}

    estudiantes = response_estudiantes.json()
    lista_ids = [est["estudianteId"] for est in estudiantes]

    # 3. Obtener calificaciones por cada estudiante
    dfs_notas = []
    for estudiante_id in lista_ids:
        url_notas = f"https://cesde-academic-app-development.up.railway.app/calificacion/estudiante/{estudiante_id}"
        response = requests.get(url_notas)
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                df["estudianteId"] = estudiante_id
                dfs_notas.append(df)

    if not dfs_notas:
        return {"error": "No hay calificaciones para este grupo"}

    # 4. Unir y resumir
    df_notas = pd.concat(dfs_notas, ignore_index=True)

    resumen = df_notas.groupby("estudianteId").agg(
        cantidad_notas=pd.NamedAgg(column="nota", aggfunc="count"),
        promedio_nota=pd.NamedAgg(column="nota", aggfunc="mean")
    ).reset_index()

    return resumen.to_dict(orient="records")
