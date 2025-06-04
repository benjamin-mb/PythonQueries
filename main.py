from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from estudiantes.estudiante_one import analizar_estudiante_one
from estudiantes.estudiante_two import analizar_estudiante_two
from estudiantes.estudiante_three import analizar_calificaciones_estudiante_three

from docentes.docente_one import docente_promedios_grupo_one
from docentes.docente_two import docente_obetener_estudiantes_en_riesgo_asistencia_two
from docentes.docente_three import docentes_porcentajes_de_estado_por_grupo_three

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o especifica tu dominio React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/estudiantes/{id}/asistencias")
def get_estudiante_asistencias_one(id: int):
    return analizar_estudiante_one(id)

@app.get("/estudiantes/{id}/asistencias")
def get_estudiantes_asistencias_two(id: int):
    return analizar_estudiante_two(id)

@app.get("/estudiantes/{id}/califiaciones")
def get_estudiante_calificaciones_three(id: int):
    return analizar_calificaciones_estudiante_three(id)


@app.get("/docentes/1/notas")
def get_docentes_notas_grupo_one():
    return docente_promedios_grupo_one()

@app.get("docentes/2/asistencia")
def get_docentes_riesgo_asistencia():
    return docente_obetener_estudiantes_en_riesgo_asistencia_two()

@app.get("docentes/3/aistencias/porcentajes")
def get_porcentaje_estado_asistencias_three():
    return docentes_porcentajes_de_estado_por_grupo_three()

# Servidor Uvicorn para ejecutar directamente con `python main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)