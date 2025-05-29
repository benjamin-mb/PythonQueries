import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#cuantos estudiantes hay por escuela

Usuarios_URL="https://cesde-academic-app-development.up.railway.app/usuario/lista"
Usuarios_response=requests.get(Usuarios_URL,auth=HTTPBasicAuth("12344321", "DevUser123"))
data_usuarios=Usuarios_response.json()
df_usuarios=pd.DataFrame(data_usuarios)

Escuelas_URL="https://cesde-academic-app-development.up.railway.app/escuela/lista"
Escuela_Response=requests.get(Escuelas_URL,auth=HTTPBasicAuth("12344321", "DevUser123"))
data_escuelas=Escuela_Response.json()
df_escuelas=pd.DataFrame(data_escuelas)


Programas_URL="https://cesde-academic-app-development.up.railway.app/programa/lista"
ProgramasResponse=requests.get(Programas_URL,auth=HTTPBasicAuth("12344321", "DevUser123"))
data_Programas=ProgramasResponse.json()
df_programas=pd.DataFrame(data_Programas)


Grupos_URL="https://cesde-academic-app-development.up.railway.app/grupo/lista"
GrupoResponse=requests.get(Grupos_URL,auth=HTTPBasicAuth("12344321", "DevUser123"))
data_Grupo=GrupoResponse.json()
df_grupos=pd.DataFrame(data_Grupo)

# 2. Filtrar solo estudiantes activos
GrupoEstudiante_URL="https://cesde-academic-app-development.up.railway.app/grupo-estudiante/lista"
GrupoEstudiante_Response=requests.get(GrupoEstudiante_URL,auth=HTTPBasicAuth("12344321", "DevUser123"))
data_grupoEstudiante=GrupoEstudiante_Response.json()
df_grupo_estudiante=pd.DataFrame(data_grupoEstudiante)


# 1. Unir grupo-estudiante con usuarios
df_ge_usuarios = df_grupo_estudiante.merge(df_usuarios, left_on="estudianteId", right_on="id")

# 2. Filtrar solo estudiantes activos
df_activos = df_ge_usuarios[df_ge_usuarios["estado"] == "ACTIVO"]

# 3. Unir con grupos para obtener nombre del programa
df_activos_grupo = df_activos.merge(df_grupos, left_on="grupoId", right_on="id", suffixes=('', '_grupo'))

# 4. Unir con programas para obtener la escuela
df_activos_full = df_activos_grupo.merge(df_programas, left_on="programa", right_on="nombre", suffixes=('', '_programa'))

# 5. Contar estudiantes activos por escuela
conteo = df_activos_full.groupby("escuela").size().reset_index(name="cantidad_estudiantes_activos")

# 7. Unir con todas las escuelas (para incluir las de cero estudiantes)
df_resultado = df_escuelas[["nombre"]].merge(conteo, left_on="nombre", right_on="escuela", how="left")

# 8. Rellenar NaN con 0 y limpiar
df_resultado["cantidad_estudiantes_activos"] = df_resultado["cantidad_estudiantes_activos"].fillna(0).astype(int)
df_resultado = df_resultado.rename(columns={"nombre": "escuela"}).drop(columns=["escuela_y"], errors='ignore')

# 9. Mostrar resultado final
print(df_resultado)
