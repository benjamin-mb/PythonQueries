import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Distribución de estudiantes por grupo


Grupos_URL="https://cesde-academic-app-development.up.railway.app/grupo/lista"
GrupoResponse=requests.get(Grupos_URL)
data_Grupo=GrupoResponse.json()
df_grupos=pd.DataFrame(data_Grupo)

GrupoEstudiante_URL="https://cesde-academic-app-development.up.railway.app/grupo-estudiante/lista"
GrupoEstudiante_Response=requests.get(GrupoEstudiante_URL)
data_grupoEstudiante=GrupoEstudiante_Response.json()
df_grupo_estudiante=pd.DataFrame(data_grupoEstudiante)

Programas_URL="https://cesde-academic-app-development.up.railway.app/programa/lista"
ProgramasResponse=requests.get(Programas_URL)
data_Programas=ProgramasResponse.json()
df_programas=pd.DataFrame(data_Programas)

Clases_URL="https://cesde-academic-app-development.up.railway.app/clase/lista"
response_clase=requests.get(Clases_URL)
data_clases=response_clase.json()
df_clases=pd.DataFrame(data_clases)

Asistencia_URL="https://cesde-academic-app-development.up.railway.app/asistencia/lista"
response_asistencia=requests.get(Asistencia_URL)
data_asistencias=response_asistencia.json()
df_asistencias=pd.DataFrame(data_asistencias)

estudiantes_por_grupo = df_grupo_estudiante['grupoId'].value_counts().reset_index()
estudiantes_por_grupo.columns = ['grupoId', 'total_estudiantes']
grupo_nombres = df_grupos[['id', 'codigo']].rename(columns={'id': 'grupoId'})
estudiantes_por_grupo = estudiantes_por_grupo.merge(grupo_nombres, on='grupoId')

plt.figure(figsize=(10, 6))
sns.barplot(data=estudiantes_por_grupo, x='total_estudiantes', y='codigo', palette='coolwarm')
plt.title('Cantidad de Estudiantes por Grupo')
plt.xlabel('Total de Estudiantes')
plt.ylabel('Código del Grupo')
plt.tight_layout()
plt.show()