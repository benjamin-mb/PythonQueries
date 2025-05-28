import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#cuantas clases tiene el docente y cual es la cantidad de estudiantes?

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
print()

codigos_grupo = df_clases["grupo"].tolist()
print(codigos_grupo)


# Lista donde guardaremos los IDs reales
ids_grupos = []


# 4. Recorer el array para obtener los id de los grupos
for code in codigos_grupo:
    GrupoCodigo_URL=f"https://cesde-academic-app-development.up.railway.app/grupo/buscar/codigo/{code}"
    response = requests.get(GrupoCodigo_URL)
    
    if response.status_code == 200:
        data = response.json()
        id_grupo = data[0].get("id")
        if id_grupo is not None:
            ids_grupos.append(id_grupo)
            print(f"{code} → ID {id_grupo}")
        else:
            print(f"{code} no tiene 'id' en la respuesta")
    else:
        print(f"Error al consultar el grupo {code}: {response.status_code}")

# Diccionario para almacenar los resultados
estudiantes_por_grupo = {}

# Recorremos los IDs de grupo
for idGrupo in ids_grupos:
    url = f"https://cesde-academic-app-development.up.railway.app/grupo-estudiante/grupo/{idGrupo}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        num_estudiantes = len(data)  # Cada item es un estudiante
        estudiantes_por_grupo[idGrupo] = num_estudiantes
        
    else:
        print(f"Error al consultar el grupo {idGrupo}: {response.status_code}")
        estudiantes_por_grupo[idGrupo] = 0

# Convertimos a DataFrame para visualizar o graficar
df_estudiantes = pd.DataFrame(list(estudiantes_por_grupo.items()), columns=["Grupo_ID", "Cantidad_Estudiantes"])

sns.barplot(data=df_estudiantes, x="Grupo_ID", y="Cantidad_Estudiantes")
plt.title("Cantidad de estudiantes por grupo")
plt.xlabel("ID del Grupo")
plt.ylabel("Cantidad de Estudiantes")
plt.tight_layout()
plt.show()

    

