import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

# Evolución de asistencias por fecha
def analizar_estudiante_two():
    # Autenticación básica
    auth = HTTPBasicAuth("12344321", "DevUser123")

    # 1. Obtener los datos desde el endpoint protegido usando auth
    Asistencia_URL = "https://cesde-academic-app-development.up.railway.app/asistencia/estudiante/13"
    response = requests.get(Asistencia_URL, auth=auth)

    # 2. Convertir respuesta JSON a DataFrame
    data = response.json()
    df = pd.DataFrame(data)

    # Convertir 'fecha' a datetime
    df['fecha'] = pd.to_datetime(df['fecha'])

    # Filtrar solo inasistencias
    inasistencias = df[df['estado'] == 'INASISTENCIA']

    # Contar inasistencias por fecha
    conteo_por_fecha = inasistencias.groupby('fecha').size()

    # Convertir fechas a string y valores a int para que sea JSON serializable
    conteo_dict = {
        fecha.strftime('%Y-%m-%d'): int(cantidad)
        for fecha, cantidad in conteo_por_fecha.items()
    }

    return conteo_dict
