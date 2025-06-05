import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

#Cuál es el promedio de notas de mis estudiantes por asignatura?

def docente_promedios_grupo_one(docenteId: int):
    auth = HTTPBasicAuth("12344321", "DevUser123")

    # 1. Obtener clases del docente
    url_clases = f"https://cesde-academic-app-development.up.railway.app/clase/docente/{docenteId}"
    response_clases = requests.get(url_clases, auth=auth)
    if response_clases.status_code != 200:
        return {"error": "No se pudieron obtener las clases del docente"}

    data_clases = response_clases.json()
    if not data_clases:
        return {"error": "El docente no tiene clases asignadas"}

    # 2. Obtener todos los códigos de grupo únicos
    codigos_grupo = list(set(clase["grupo"] for clase in data_clases))

    # 3. Obtener IDs de grupo
    ids_grupo = []
    for codigo in codigos_grupo:
        url_grupo = f"https://cesde-academic-app-development.up.railway.app/grupo/buscar/codigo/{codigo}"
        response_grupo = requests.get(url_grupo, auth=auth)
        if response_grupo.status_code == 200 and response_grupo.json():
            grupo_id = response_grupo.json()[0]["id"]
            ids_grupo.append((codigo, grupo_id))

    if not ids_grupo:
        return {"error": "No se encontraron IDs para los grupos del docente"}

    # 4. Obtener estudiantes por cada grupo
    estudiantes_total = []
    for codigo, grupo_id in ids_grupo:
        url_estudiantes = f"https://cesde-academic-app-development.up.railway.app/grupo-estudiante/grupo/{grupo_id}"
        response_estudiantes = requests.get(url_estudiantes, auth=auth)
        if response_estudiantes.status_code == 200:
            estudiantes = response_estudiantes.json()
            for est in estudiantes:
                est["grupo_codigo"] = codigo
                est["grupo_id"] = grupo_id
            estudiantes_total.extend(estudiantes)

    if not estudiantes_total:
        return {"error": "No se encontraron estudiantes en los grupos"}

    # 5. Obtener notas por cada estudiante
    dfs_notas = []
    for est in estudiantes_total:
        estudiante_id = est["estudianteId"]
        grupo_codigo = est["grupo_codigo"]

        url_notas = f"https://cesde-academic-app-development.up.railway.app/calificacion/estudiante/{estudiante_id}"
        response_notas = requests.get(url_notas, auth=auth)
        if response_notas.status_code == 200:
            data = response_notas.json()
            if data:
                df = pd.DataFrame(data)
                df["estudianteId"] = estudiante_id
                df["grupo_codigo"] = grupo_codigo
                dfs_notas.append(df)

    if not dfs_notas:
        return {"error": "No hay calificaciones registradas"}

    # 6. Concatenar todo y calcular promedios por estudiante y grupo
    df_notas = pd.concat(dfs_notas, ignore_index=True)

    resumen = df_notas.groupby(["grupo_codigo", "estudianteId"]).agg(
        cantidad_notas=pd.NamedAgg(column="nota", aggfunc="count"),
        promedio_nota=pd.NamedAgg(column="nota", aggfunc="mean")
    ).reset_index()

    return resumen.to_dict(orient="records")


