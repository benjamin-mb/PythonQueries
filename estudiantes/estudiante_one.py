import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

def analizar_estudiante_one():
    # Autenticación básica
    auth = HTTPBasicAuth("12344321", "DevUser123")

    # 1. Obtener los datos desde el endpoint protegido usando auth
    url = "https://cesde-academic-app-development.up.railway.app/asistencia/estudiante/13"
    response = requests.get(url, auth=auth)

    # 2. Convertir respuesta JSON a DataFrame
    data = response.json()
    df = pd.DataFrame(data)

    # 3. Convertir columna 'fecha' a datetime
    df['fecha'] = pd.to_datetime(df['fecha'])

    # 4. Filtrar datos entre enero y junio de 2025
    inicio = pd.Timestamp('2025-01-01')
    fin = pd.Timestamp('2025-06-30')
    df_filtrado = df[(df['fecha'] >= inicio) & (df['fecha'] <= fin)]

    # 5. Contar cuántas veces aparece cada estado (ASISTENCIA, INASISTENCIA, etc.)
    conteo_estados = df_filtrado['estado'].value_counts().to_dict()

    # 6. Devolver el resultado para que React lo grafique
    return conteo_estados
