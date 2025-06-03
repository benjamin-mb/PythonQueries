import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

def docente_obetener_estudiantes_en_riesgo_asistencia_two():
    # Autenticación fija
    auth = HTTPBasicAuth("12344321", "DevUser123")

    # Paso 1: Obtener los docentes (no se usa el resultado, pero lo dejamos como está)
    Docentes_URL = "https://cesde-academic-app-development.up.railway.app/usuario/buscar/tipo/DOCENTE"
    requests.get(Docentes_URL, auth=auth)

    # Paso 2: Obtener las clases del docente 101
    Clases_URL = "https://cesde-academic-app-development.up.railway.app/clase/docente/101"
    requests.get(Clases_URL, auth=auth)

    # Paso 3: Código del grupo
    codigoGrupo = 'P1-S2025-1-1'
    GrupoCodigo_URL = f"https://cesde-academic-app-development.up.railway.app/grupo/buscar/codigo/{codigoGrupo}"
    response_grupo = requests.get(GrupoCodigo_URL, auth=auth)
    data_grupo = response_grupo.json()
    idGrupo = data_grupo[0]['id']

    # Paso 4: Obtener estudiantes del grupo
    GrupoID_URL = f"https://cesde-academic-app-development.up.railway.app/grupo-estudiante/grupo/{idGrupo}"
    response_estudiantes = requests.get(GrupoID_URL)
    data_estudiantes = response_estudiantes.json()
    df_estudiantes = pd.DataFrame(data_estudiantes)
    lista_estudiantes_ids = df_estudiantes["estudianteId"].tolist()

    # Paso 5: Recorrer estudiantes y juntar asistencias
    df_Asistencias_total = []

    for estudianteId in lista_estudiantes_ids:
        url_asistencias = f"https://cesde-academic-app-development.up.railway.app/asistencia/estudiante/{estudianteId}"
        response = requests.get(url_asistencias)

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
