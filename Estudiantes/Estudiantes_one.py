import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

#inacistencias y asistencias en el semestre y en el mes
#id 13

Asistencia_URL="https://cesde-academic-app-development.up.railway.app/asistencia/estudiante/13"
responseAsistenciaEstudiante=requests.get(Asistencia_URL)
dataAsistencia=responseAsistenciaEstudiante.json()
df_AsistenciaEstudiante=pd.DataFrame(dataAsistencia)

# Convertir la columna 'fecha' a tipo datetime
df_AsistenciaEstudiante['fecha'] = pd.to_datetime(df_AsistenciaEstudiante['fecha'])

# Filtrar asistencias entre enero y junio de 2025
inicio = pd.Timestamp('2025-01-01')
fin = pd.Timestamp('2025-06-30')
df_filtrado = df_AsistenciaEstudiante[(df_AsistenciaEstudiante['fecha'] >= inicio) & (df_AsistenciaEstudiante['fecha'] <= fin)]

# Contar cuántas veces aparece cada estado (ASISTENCIA, INASISTENCIA, etc.)
conteo_estados = df_filtrado['estado'].value_counts()

# Crear el gráfico de pastel
plt.figure(figsize=(6, 6))
plt.pie(conteo_estados, labels=conteo_estados.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Set3.colors)
plt.title('Distribución de asistencias (Ene-Jun 2025)')
plt.axis('equal')  # Asegura que el gráfico sea un círculo
plt.show()


