import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from requests.auth import HTTPBasicAuth
# Evolución de asistencias por fecha
#id 13

Asistencia_URL="https://cesde-academic-app-development.up.railway.app/asistencia/estudiante/13"
responseAsistenciaEstudiante=requests.get(Asistencia_URL,auth=HTTPBasicAuth("12344321", "DevUser123"))
dataAsistencia=responseAsistenciaEstudiante.json()
df_AsistenciaEstudiante=pd.DataFrame(dataAsistencia)

# Convertir 'fecha' a datetime
df_AsistenciaEstudiante['fecha'] = pd.to_datetime(df_AsistenciaEstudiante['fecha'])

# Filtrar solo inasistencias
inasistencias = df_AsistenciaEstudiante[df_AsistenciaEstudiante['estado'] == 'INASISTENCIA']

# Contar inasistencias por fecha
conteo_por_fecha = inasistencias.groupby('fecha').size()


# Gráfico de líneas
plt.figure(figsize=(10, 5))
sns.lineplot(data=conteo_por_fecha, marker='o', color='red')
plt.title('Evolución de inasistencias por fecha')
plt.xlabel('Fecha')
plt.ylabel('Cantidad de inasistencias')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()