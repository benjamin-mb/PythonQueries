import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Distribución de estudiantes por grupo


Grupos_URL="https://cesde-academic-app-development.up.railway.app/grupo/lista"
GrupoResponse=requests.get(Grupos_URL,auth=HTTPBasicAuth("12344321", "DevUser123"))
data_Grupo=GrupoResponse.json()
df_grupos=pd.DataFrame(data_Grupo)

GrupoEstudiante_URL="https://cesde-academic-app-development.up.railway.app/grupo-estudiante/lista"
GrupoEstudiante_Response=requests.get(GrupoEstudiante_URL,auth=HTTPBasicAuth("12344321", "DevUser123"))
data_grupoEstudiante=GrupoEstudiante_Response.json()
df_grupo_estudiante=pd.DataFrame(data_grupoEstudiante)

Programas_URL="https://cesde-academic-app-development.up.railway.app/programa/lista"
ProgramasResponse=requests.get(Programas_URL,auth=HTTPBasicAuth("12344321", "DevUser123"))
data_Programas=ProgramasResponse.json()
df_programas=pd.DataFrame(data_Programas)

Clases_URL="https://cesde-academic-app-development.up.railway.app/clase/lista"
response_clase=requests.get(Clases_URL,auth=HTTPBasicAuth("12344321", "DevUser123"))
data_clases=response_clase.json()
df_clases=pd.DataFrame(data_clases)

Asistencia_URL="https://cesde-academic-app-development.up.railway.app/asistencia/lista"
response_asistencia=requests.get(Asistencia_URL,auth=HTTPBasicAuth("12344321", "DevUser123"))
data_asistencias=response_asistencia.json()
df_asistencias=pd.DataFrame(data_asistencias)

estudiantes_por_grupo = df_grupo_estudiante['grupoId'].value_counts().reset_index()
estudiantes_por_grupo.columns = ['grupoId', 'total_estudiantes']
grupo_nombres = df_grupos[['id', 'codigo']].rename(columns={'id': 'grupoId'})
estudiantes_por_grupo = estudiantes_por_grupo.merge(grupo_nombres, on='grupoId')

plt.figure(figsize=(10, 6))
sns.barplot(data=estudiantes_por_grupo, x='total_estudiantes', y='codigo', palette='coolwarm')
plt.title('Cantidad de estudiantes por Grupo')
plt.xlabel('Total de estudiantes')
plt.ylabel('Código del Grupo')
plt.tight_layout()
plt.show()