import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Asistencias por programa


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

df_asistencias = pd.concat([df_asistencias.drop('clase', axis=1), df_asistencias['clase'].apply(pd.Series)], axis=1)

resumen = df_asistencias.groupby(['grupo', 'docente', 'modulo', 'estado']).size().reset_index(name='total')

print(resumen)


plt.figure(figsize=(12, 7)) 
sns.barplot(
    data=resumen,
    x='total',
    y='grupo',
    hue='estado',
    palette='pastel'
)

plt.title("Asistencia por Grupo y Estado", fontsize=16)
plt.xlabel("Cantidad")
plt.ylabel("Grupo")
plt.tight_layout()
plt.show()
