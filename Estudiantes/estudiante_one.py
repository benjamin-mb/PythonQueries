import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

def analizar_asistencia_estudiante_13():
    # 1. Obtener datos desde el endpoint
    url = "https://cesde-academic-app-development.up.railway.app/asistencia/estudiante/13"
    auth = HTTPBasicAuth("12344321", "DevUser123")
    response = requests.get(url, auth=auth)
    data = response.json()
    df = pd.DataFrame(data)

    # 2. Convertir fecha a datetime y filtrar por rango
    df['fecha'] = pd.to_datetime(df['fecha'])
    inicio = pd.Timestamp('2025-01-01')
    fin = pd.Timestamp('2025-06-30')
    df_filtrado = df[(df['fecha'] >= inicio) & (df['fecha'] <= fin)]

    # 3. Contar estados (ASISTENCIA, INASISTENCIA, etc.)
    conteo = df_filtrado['estado'].value_counts().to_dict()

    
    # 4. Devolver en formato JSON (React puede graficar esto)
    return conteo

print(analizar_asistencia_estudiante_13())
