import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

def administrativo_distribucion_estudiantes_por_grupo_two():
    # 1. Cargar datos
    auth = HTTPBasicAuth("12344321", "DevUser123")

    grupo_estudiante_url = "https://cesde-academic-app-development.up.railway.app/grupo-estudiante/lista"
    grupos_url = "https://cesde-academic-app-development.up.railway.app/grupo/lista"

    df_grupo_est = pd.DataFrame(requests.get(grupo_estudiante_url, auth=auth).json())
    df_grupos = pd.DataFrame(requests.get(grupos_url, auth=auth).json())

    # Validación para evitar errores si los datos vienen vacíos
    if df_grupo_est.empty or df_grupos.empty:
        return {"error": "Datos vacíos de grupo o grupo-estudiante"}

    # 2. Agrupar: contar estudiantes por grupoId
    estudiantes_por_grupo = df_grupo_est['grupoId'].value_counts().reset_index()
    estudiantes_por_grupo.columns = ['grupoId', 'total_estudiantes']

    # 3. Unir con los códigos de grupo
    grupos_codigos = df_grupos[['id', 'codigo']].rename(columns={'id': 'grupoId'})
    resultado = estudiantes_por_grupo.merge(grupos_codigos, on='grupoId', how='left')

    # 4. Convertir a lista de diccionarios para retornar como JSON
    return resultado.to_dict(orient='records')
