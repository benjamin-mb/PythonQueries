import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

def analizar_calificaciones_estudiante_three():
    estudianteId = 13
    url = f"https://cesde-academic-app-development.up.railway.app/calificacion/estudiante/{estudianteId}"
    auth = HTTPBasicAuth("12344321", "DevUser123")

    # 1. Llamar al endpoint
    response = requests.get(url, auth=auth)
    data = response.json()

    # 2. Crear DataFrame
    df = pd.DataFrame(data)

    # Validar si hay datos
    if df.empty:
        return {"mensaje": "No hay calificaciones registradas para el estudiante."}

    # 3. Convertir fechas
    df['fecha'] = pd.to_datetime(df['fecha'])

    # 4. Ordenar por fecha
    df = df.sort_values('fecha')

    # 5. Seleccionar campos clave y devolver
    resultado = df[['fecha', 'nota', 'actividad']].to_dict(orient='records')
    return resultado
