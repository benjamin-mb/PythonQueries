import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

# Evolución de asistencias por fecha

def analizar_estudiante_two():
    # Autenticación básica
    auth = HTTPBasicAuth("12344321", "DevUser123")

    # 1. Obtener los datos desde el endpoint protegido usando auth
    Asistencia_URL="https://cesde-academic-app-development.up.railway.app/asistencia/estudiante/13"
    responseAsistencia=requests.get(Asistencia_URL,auth=auth)

    # 2. Convertir respuesta JSON a DataFrame
    data=responseAsistencia.json()
    df_AsistenciaEstudiante=pd.DataFrame(data)

    # Convertir 'fecha' a datetime
    df_AsistenciaEstudiante['fecha'] = pd.to_datetime(df_AsistenciaEstudiante['fecha'])

    # Filtrar solo inasistencias
    inasistencias = df_AsistenciaEstudiante[df_AsistenciaEstudiante['estado'] == 'INASISTENCIA']

    # Contar inasistencias por fecha
    conteo_por_fecha = inasistencias.groupby('fecha').size()

    return conteo_por_fecha


