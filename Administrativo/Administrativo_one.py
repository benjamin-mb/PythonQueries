import requests
from requests.auth import HTTPBasicAuth
import pandas as pd


# Distribución de estudiantes por programa


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

programa_estudiantes = df_grupo_estudiante.groupby('grupoId').size().reset_index(name='total_estudiantes')
grupos_info = df_grupos[['id', 'programa']].rename(columns={'id': 'grupoId'})
programa_estudiantes = programa_estudiantes.merge(grupos_info, on='grupoId')
programa_distribucion = programa_estudiantes.groupby('programa')['total_estudiantes'].sum().reset_index()

# Gráfico
#plt.figure(figsize=(10, 6))
#sns.barplot(data=programa_distribucion, x='total_estudiantes', y='programa', palette='Blues_d')
#plt.title('Cantidad de Estudiantes por Programa')
#plt.xlabel('Total de Estudiantes')
#plt.ylabel('Programa')
#plt.tight_layout()
#plt.show()
