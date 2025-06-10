from fastapi.responses import JSONResponse
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

def directivo_obtener_estudiantes_activos_por_escuela_three():
    try:
        # Autenticación
        auth = HTTPBasicAuth("12344321", "DevUser123")

        # Endpoints
        urls = {
            "usuarios": "https://cesde-academic-app-development.up.railway.app/usuario/lista",
            "escuelas": "https://cesde-academic-app-development.up.railway.app/escuela/lista",
            "programas": "https://cesde-academic-app-development.up.railway.app/programa/lista",
            "grupos": "https://cesde-academic-app-development.up.railway.app/grupo/lista",
            "grupo_estudiante": "https://cesde-academic-app-development.up.railway.app/grupo-estudiante/lista"
        }

        # Descargar datos
        df_usuarios = pd.DataFrame(requests.get(urls["usuarios"], auth=auth).json())
        df_escuelas = pd.DataFrame(requests.get(urls["escuelas"], auth=auth).json())
        df_programas = pd.DataFrame(requests.get(urls["programas"], auth=auth).json())
        df_grupos = pd.DataFrame(requests.get(urls["grupos"], auth=auth).json())
        df_grupo_estudiante = pd.DataFrame(requests.get(urls["grupo_estudiante"], auth=auth).json())

        # Unión grupo-estudiante con usuarios
        df_ge_usuarios = df_grupo_estudiante.merge(df_usuarios, left_on="estudianteId", right_on="id")

        # Filtrar estudiantes activos
        df_activos = df_ge_usuarios[df_ge_usuarios["estado"] == "ACTIVO"]

        # Unir con grupos y luego con programas
        df_activos_grupo = df_activos.merge(df_grupos, left_on="grupoId", right_on="id", suffixes=('', '_grupo'))
        df_activos_full = df_activos_grupo.merge(
            df_programas, left_on="programa", right_on="nombre", suffixes=('', '_programa')
        )

        # Conteo por escuela
        conteo = df_activos_full.groupby("escuela").size().reset_index(name="cantidad_estudiantes_activos")

        # Unión con todas las escuelas
        df_resultado = df_escuelas[["nombre"]].merge(conteo, left_on="nombre", right_on="escuela", how="left")

        # Rellenar NaNs con 0
        df_resultado["cantidad_estudiantes_activos"] = df_resultado["cantidad_estudiantes_activos"].fillna(0).astype(int)

        # Renombrar columna
        df_resultado = df_resultado.rename(columns={"nombre": "escuela"}).drop(columns=["escuela_y"], errors="ignore")

        # Asegurar que no haya NaNs
        df_resultado = df_resultado.fillna(0)

        # Convertir a lista de diccionarios
        resultado = df_resultado.to_dict(orient="records")

        return JSONResponse(content=resultado)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
