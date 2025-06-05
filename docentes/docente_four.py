import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

#Cuál es el promedio de notas de mis estudiantes por asignatura?

def docente_promedio_notas_por_asignatura_four(docente_id: int):
    auth = HTTPBasicAuth("12344321", "DevUser123")

    # 1. Obtener clases del docente
    url_clases = f"https://cesde-academic-app-development.up.railway.app/clase/docente/{docente_id}"
    response_clases = requests.get(url_clases, auth=auth)
    if response_clases.status_code != 200:
        return {"error": "No se pudieron obtener las clases del docente"}

    data_clases = response_clases.json()
    if not data_clases:
        return {"error": "El docente no tiene clases asignadas"}

    df_clases = pd.DataFrame(data_clases)
    
    # 2. Obtener códigos de grupo y módulos únicos
    grupos_modulos = df_clases[["grupo", "modulo"]].drop_duplicates().to_dict(orient="records")

    resultados = []

    for item in grupos_modulos:
        codigo_grupo = item["grupo"]
        modulo = item["modulo"]

        # 3. Obtener ID del grupo
        url_grupo = f"https://cesde-academic-app-development.up.railway.app/grupo/buscar/codigo/{codigo_grupo}"
        response_grupo = requests.get(url_grupo, auth=auth)
        if response_grupo.status_code != 200 or not response_grupo.json():
            continue

        id_grupo = response_grupo.json()[0]["id"]

        # 4. Obtener estudiantes del grupo
        url_estudiantes = f"https://cesde-academic-app-development.up.railway.app/grupo-estudiante/grupo/{id_grupo}"
        response_estudiantes = requests.get(url_estudiantes, auth=auth)
        if response_estudiantes.status_code != 200:
            continue

        estudiantes = response_estudiantes.json()
        estudiante_ids = [est["estudianteId"] for est in estudiantes]

        # 5. Obtener notas de cada estudiante
        dfs_notas = []
        for estudiante_id in estudiante_ids:
            url_notas = f"https://cesde-academic-app-development.up.railway.app/calificacion/estudiante/{estudiante_id}"
            response_notas = requests.get(url_notas, auth=auth)
            if response_notas.status_code == 200:
                data_notas = response_notas.json()
                df_notas = pd.DataFrame(data_notas)
                if not df_notas.empty:
                    df_notas["estudianteId"] = estudiante_id
                    dfs_notas.append(df_notas)

        if not dfs_notas:
            continue

        df_total_notas = pd.concat(dfs_notas, ignore_index=True)

        # 6. Calcular promedio por estudiante
        df_resumen = df_total_notas.groupby("estudianteId").agg(
            cantidad_notas=pd.NamedAgg(column="nota", aggfunc="count"),
            promedio_nota=pd.NamedAgg(column="nota", aggfunc="mean")
        ).reset_index()

        # 7. Calcular promedio general del grupo en ese módulo
        promedio_general = round(df_resumen["promedio_nota"].mean(), 2)
        cantidad_estudiantes = df_resumen.shape[0]

        resultados.append({
            "grupo": codigo_grupo,
            "modulo": modulo,
            "promedio_general": promedio_general,
            "estudiantes_con_notas": cantidad_estudiantes
        })

    if not resultados:
        return {"mensaje": "No se encontraron notas en los grupos del docente."}

    return resultados
