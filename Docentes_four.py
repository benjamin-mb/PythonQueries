import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



##Cuál es el promedio de notas de mis estudiantes por asignatura?

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
#print(dataClase)

codigoGrupo='P1-S2025-1-1'


#por el codigo del grupo busco en el endpoint el id
GrupoCodigo_URL=f"https://cesde-academic-app-development.up.railway.app/grupo/buscar/codigo/{codigoGrupo}"
responseGrupoPorCodigo=requests.get(GrupoCodigo_URL)
dataGroupdGetId=responseGrupoPorCodigo.json()
df_group=pd.DataFrame(dataGroupdGetId)
#print(dataGroupdGetId)

idGrupo=dataGroupdGetId[0]['id']

#busco en el endpoint los estudientes por grupo
GrupoID_URL=f"https://cesde-academic-app-development.up.railway.app/grupo-estudiante/grupo/{idGrupo}"
responseEstudiantesGrupo=requests.get(GrupoID_URL)
dataEstudiantesporGroupId=responseEstudiantesGrupo.json()
df_EstudiantesGrupoPorId=pd.DataFrame(dataEstudiantesporGroupId)
# print(dataEstudiantesporGroupId)

#creo una lista para guardar los id de los estudiantes
listaEstudiantes_ids = df_EstudiantesGrupoPorId["estudianteId"].tolist()

dfs_notas = []


for estudianteId in listaEstudiantes_ids:
    NotasPorIDEstudiante_URL=f"https://cesde-academic-app-development.up.railway.app/calificacion/estudiante/{estudianteId}"
    response = requests.get(NotasPorIDEstudiante_URL)
    
    if response.status_code == 200:
        dataNotasEstudiantes = response.json()
        df_notas = pd.DataFrame(dataNotasEstudiantes)
        
        # Agregamos el ID del estudiante al DataFrame si no viene
        if not df_notas.empty:
            df_notas["estudianteId"] = estudianteId
            dfs_notas.append(df_notas)
    else:
        print(f"Error al obtener notas para estudiante {estudianteId}")

# Combinar todas las notas en un solo DataFrame
df_todas_las_notas = pd.concat(dfs_notas, ignore_index=True)

# Mostrar
# print(df_todas_las_notas)

# Agrupamos por estudianteId para contar y calcular promedio
df_resumen_notas = df_todas_las_notas.groupby("estudianteId").agg(
    cantidad_notas=pd.NamedAgg(column="nota", aggfunc="count"),
    promedio_nota=pd.NamedAgg(column="nota", aggfunc="mean")
).reset_index()

# Categorizar rendimiento según promedio de nota
def categorizar_promedio(promedio):
    if promedio <= 2.9:
        return "Bajo"
    elif promedio < 4:
        return "Medio"
    else:
        return "Alto"

df_resumen_notas["categoria"] = df_resumen_notas["promedio_nota"].apply(categorizar_promedio)

# Contar cuántos estudiantes hay en cada categoría
conteo_categorias = df_resumen_notas["categoria"].value_counts()
print(conteo_categorias)

# Labels y tamaños para pie chart
labels = conteo_categorias.index.tolist()
sizes = conteo_categorias.values.tolist()

plt.figure(figsize=(6,6))
plt.pie(
    sizes,
    labels=labels,
    autopct='%1.1f%%',
    startangle=90,
    colors=sns.color_palette("pastel")
)
plt.title("Distribución de estudiantes según promedio de notas")
plt.tight_layout()
plt.show()
j