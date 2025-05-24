import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#¿Qué estudiantes están en riesgo académico  muchas inasistencias?*

##accedo a docentes
Docentes_URL="https://cesde-academic-app-development.up.railway.app/usuario/buscar/tipo/DOCENTE"
responseDocentes=requests.get(Docentes_URL)
dataDocente=responseDocentes.json()
df_docentes = pd.DataFrame(dataDocente)

##accedo a las clases para obetener el codigo del grupo
Clases_URL="https://cesde-academic-app-development.up.railway.app/clase/docente/101"
responseClases=requests.get(Clases_URL)
dataClase=responseClases.json()
df_clases =pd.DataFrame(dataClase)

codigoGrupo='P1-S2025-1-1'

#por el codigo del grupo busco en el endpoint el id
GrupoCodigo_URL=f"https://cesde-academic-app-development.up.railway.app/grupo/buscar/codigo/{codigoGrupo}"
responseGrupoPorCodigo=requests.get(GrupoCodigo_URL)
dataGroupdGetId=responseGrupoPorCodigo.json()
df_group=pd.DataFrame(dataGroupdGetId)

idGrupo=dataGroupdGetId[0]['id']

#busco en el endpoint los estudientes por grupo
GrupoID_URL=f"https://cesde-academic-app-development.up.railway.app/grupo-estudiante/grupo/{idGrupo}"
responseEstudiantesGrupo=requests.get(GrupoID_URL)
dataEstudiantesporGroupId=responseEstudiantesGrupo.json()
df_EstudiantesGrupoPorId=pd.DataFrame(dataEstudiantesporGroupId)
#print(dataEstudiantesporGroupId)

#creo una lista para guardar los id de los estudiantes
listaEstudiantes_ids = df_EstudiantesGrupoPorId["estudianteId"].tolist()
print(listaEstudiantes_ids)

df_Asistencias_total=[]

for EstudianteId in listaEstudiantes_ids:
    AsistenciaPorId_URL=f"https://cesde-academic-app-development.up.railway.app/asistencia/estudiante/{EstudianteId}"
    response = requests.get(AsistenciaPorId_URL)

    if response.status_code == 200:
        data_asistencias = response.json()
        df_asistencias = pd.DataFrame(data_asistencias)
        
        if not df_asistencias.empty:
            df_asistencias["estudianteId"] = EstudianteId
            df_Asistencias_total.append(df_asistencias)

# Unir todos los registros en un solo DataFrame
df_asistencias_final = pd.concat(df_Asistencias_total, ignore_index=True)

# Filtrar las inasistencias
df_inasistencias = df_asistencias_final[df_asistencias_final["estado"] == "INASISTENCIA"]

# Contar cuántas inasistencias tiene cada estudiante
df_inasistencias_count = df_inasistencias.groupby("estudianteId").size().reset_index(name="cantidad_inasistencias")

# Establecer umbral de riesgo (por ejemplo, más de 3 inasistencias)
umbral = 1
df_en_riesgo = df_inasistencias_count[df_inasistencias_count["cantidad_inasistencias"] > umbral]

# Mostrar estudiantes en riesgo
print("Estudiantes en riesgo académico por inasistencias:")
print(df_en_riesgo)

plt.figure(figsize=(10,6))
sns.barplot(
    data=df_en_riesgo,
    x='estudianteId',
    y='cantidad_inasistencias',
    palette="Blues_d"
)
plt.title("Estudiantes en riesgo")
plt.xlabel("ID Estudiante")
plt.ylabel("Cantidad de Inasistencias")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()