import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

def docente_obetener_estudiantes_en_riesgo_asistencia_two(docenteId : int):
    
    # Autenticación fija
    auth = HTTPBasicAuth("12344321", "DevUser123")

    # Paso 1: Obtener clases del docente
    url_clases = f"https://cesde-academic-app-development.up.railway.app/clase/docente/{docenteId}"
    response_clases = requests.get(url_clases, auth=auth)
    if response_clases.status_code != 200:
        return {"error": "No se pudieron obtener las clases del docente"}

    data_clases = response_clases.json()
    if not data_clases:
        return {"error": "El docente no tiene clases asignadas"}

    # Paso 2: Obtener todos los códigos de grupo únicos
    codigos_grupo = list(set(clase["grupo"] for clase in data_clases))

    # Paso 3: Obtener IDs de grupo
    ids_grupo = []
    for codigo in codigos_grupo:
        url_grupo = f"https://cesde-academic-app-development.up.railway.app/grupo/buscar/codigo/{codigo}"
        response_grupo = requests.get(url_grupo, auth=auth)
        if response_grupo.status_code == 200 and response_grupo.json():
            grupo_id = response_grupo.json()[0]["id"]
            ids_grupo.append((codigo, grupo_id))

    if not ids_grupo:
        return {"error": "No se encontraron IDs para los grupos del docente"}

    # Paso 4: Obtener estudiantes de todos los grupos
    lista_estudiantes_ids = []
    for codigo, idGrupo in ids_grupo:
        GrupoID_URL = f"https://cesde-academic-app-development.up.railway.app/grupo-estudiante/grupo/{idGrupo}"
        response_estudiantes = requests.get(GrupoID_URL, auth=auth)
        if response_estudiantes.status_code == 200:
            data_estudiantes = response_estudiantes.json()
            for est in data_estudiantes:
                lista_estudiantes_ids.append(est["estudianteId"])

    if not lista_estudiantes_ids:
        return {"mensaje": "No se encontraron estudiantes en los grupos del docente"}

    # Paso 5: Recorrer estudiantes y juntar asistencias
    df_Asistencias_total = []

    for estudianteId in lista_estudiantes_ids:
        url_asistencias = f"https://cesde-academic-app-development.up.railway.app/asistencia/estudiante/{estudianteId}"
        response = requests.get(url_asistencias, auth=auth)

        if response.status_code == 200:
            data_asistencias = response.json()
            df_asistencias = pd.DataFrame(data_asistencias)

            if not df_asistencias.empty:
                df_asistencias["estudianteId"] = estudianteId
                df_Asistencias_total.append(df_asistencias)

    # Paso 6: Unir todas las asistencias
    if not df_Asistencias_total:
        return {"mensaje": "No se encontraron asistencias para ningún estudiante."}

    df_final = pd.concat(df_Asistencias_total, ignore_index=True)

    # Paso 7: Filtrar inasistencias
    df_inasistencias = df_final[df_final["estado"] == "INASISTENCIA"]

    # Paso 8: Contar inasistencias por estudiante
    df_inasistencias_count = df_inasistencias.groupby("estudianteId").size().reset_index(name="cantidad_inasistencias")

    # Paso 9: Aplicar umbral (más de 1 inasistencia = riesgo)
    umbral = 1
    df_en_riesgo = df_inasistencias_count[df_inasistencias_count["cantidad_inasistencias"] > umbral]

    # Paso 10: Devolver como JSON
    return df_en_riesgo.to_dict(orient="records")
