import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

#Cual es el porcentaje Total de estados de asistencia

def docentes_porcentajes_de_estado_por_grupo_three():
    auth=HTTPBasicAuth("12344321", "DevUser123")
##accedo a docentes
    Docentes_URL="https://cesde-academic-app-development.up.railway.app/usuario/buscar/tipo/DOCENTE"
    responseDocentes=requests.get(Docentes_URL,auth=auth)
    dataDocente=responseDocentes.json()
    df_docentes = pd.DataFrame(dataDocente)

    ##accedo a las clases para obetener el codigo del grupo
    Clases_URL="https://cesde-academic-app-development.up.railway.app/clase/docente/101"
    responseClases=requests.get(Clases_URL,auth=auth)
    dataClase=responseClases.json()
    df_clases =pd.DataFrame(dataClase)

    codigoGrupo='P1-S2025-1-1'

    #por el codigo del grupo busco en el endpoint el id
    GrupoCodigo_URL=f"https://cesde-academic-app-development.up.railway.app/grupo/buscar/codigo/{codigoGrupo}"
    responseGrupoPorCodigo=requests.get(GrupoCodigo_URL,auth=auth)
    dataGroupdGetId=responseGrupoPorCodigo.json()
    

    idGrupo=dataGroupdGetId[0]['id']

    #busco en el endpoint los estudientes por grupo
    GrupoID_URL=f"https://cesde-academic-app-development.up.railway.app/grupo-estudiante/grupo/{idGrupo}"
    responseEstudiantesGrupo=requests.get(GrupoID_URL,auth=auth)
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

    # Contar total de asistencias e inasistencias (sin importar estudiante)
    conteo_estados = df_asistencias_final["estado"].value_counts()

    return conteo_estados
