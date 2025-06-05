import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

def docente_cantidad_estudiantes_por_clase_five(docente_id: int):
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

    # 2. Obtener combinaciones únicas de grupo y módulo
    grupos_modulos = df_clases[["grupo", "modulo", "id"]].drop_duplicates()

    resultados = []

    for _, row in grupos_modulos.iterrows():
        codigo_grupo = row["grupo"]
        modulo_nombre = row["modulo"]
        clase_id = row["id"]

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
        cantidad_estudiantes = len(estudiantes)

        resultados.append({
            "clase_id": clase_id,
            "modulo": modulo_nombre,
            "grupo_codigo": codigo_grupo,
            "cantidad_estudiantes": cantidad_estudiantes
        })

    return {"data": resultados}
