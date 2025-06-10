import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

def administrativo_get_asistencias_por_programa_three():
    # Autenticación
    auth = HTTPBasicAuth("12344321", "DevUser123")

    # Obtener datos
    df_grupos = pd.DataFrame(requests.get(
        "https://cesde-academic-app-development.up.railway.app/grupo/lista", auth=auth).json())

    df_asistencias = pd.DataFrame(requests.get(
        "https://cesde-academic-app-development.up.railway.app/asistencia/lista", auth=auth).json())

    # Desanidar campo 'clase'
    df_asistencias = pd.concat(
        [df_asistencias.drop('clase', axis=1), df_asistencias['clase'].apply(pd.Series)],
        axis=1
    )

    # Unir con programa usando grupo
    df_asistencias = df_asistencias.merge(
        df_grupos[['codigo', 'programa']],
        how='left',
        left_on='grupo',
        right_on='codigo'
    )

    # Agrupar por programa y estado
    resumen = df_asistencias.groupby(['programa', 'estado']).size().reset_index(name='total')

    # Convertir a JSON
    resultado_json = resumen.to_dict(orient='records')

    return resultado_json
