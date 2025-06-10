from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from estudiantes.estudiante_one import analizar_estudiante_one
from estudiantes.estudiante_two import analizar_estudiante_two
from estudiantes.estudiante_three import analizar_calificaciones_estudiante_three

from docentes.docente_one import docente_promedios_grupo_one
from docentes.docente_two import docente_obetener_estudiantes_en_riesgo_asistencia_two
from docentes.docente_three import docentes_porcentajes_de_estado_por_grupo_three
from docentes.docente_four import docente_promedio_notas_por_asignatura_four
from docentes.docentes_five import docente_cantidad_estudiantes_por_clase_five

from directivo.directivo_one import directivo_programas_por_escuela_uno
from directivo.directivo_two import directivo_clases_horarios_por_modulo_dos
from directivo.directivo_three import directivo_obtener_estudiantes_activos_por_escuela_three
from directivo.directivo_four import directivo_escuela_mas_programas_four

from administrativo.administrativo_one import administrativo_distribucion_estudiantes_por_programa_one

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


@app.get("/docentes/{id}/notas")
def get_docentes_notas_grupo_one(id):
    return docente_promedios_grupo_one(id)

@app.get("/docentes/{id}/asistencia")
def get_docentes_riesgo_asistencia_two(id):
    return docente_obetener_estudiantes_en_riesgo_asistencia_two(id)

@app.get("/docentes/{id}/aistencias/porcentajes")
def get_porcentaje_estado_asistencias_three(id):
    return docentes_porcentajes_de_estado_por_grupo_three(id)

@app.get("/docentes/{id}/promedio/notas")
def get_promedio_notas_por_clase(id):
    return docente_promedio_notas_por_asignatura_four(id)

@app.get("/docentes/clases/{id}/estudiantes")
def get_cantidad_de_clase_y_estudiantes_por_clase_five(id):
    return docente_cantidad_estudiantes_por_clase_five(id)

#Directivos

@app.get("/directivo/programas/escuela")
def get_cantidad_grupos_por_escuela():
    return directivo_programas_por_escuela_uno()

@app.get("/directivos/clases/modulo/horarios")
def get_cantidad_clases_por_horario_y_horarios_por_clase():
    return directivo_clases_horarios_por_modulo_dos()

@app.get("/directivos/activos/estudiantes")
def get_estudiantes_activos_por_escuela():
    return directivo_obtener_estudiantes_activos_por_escuela_three()

@app.get("/directivos/programas/escuelas")
def get_escuelas_con_mayor_cantidad_de_escuelas():
    return directivo_escuela_mas_programas_four()

#administrativo 
@app.get("/administrativo/distribucion/programa")
def get_distribucion_estudiantes_por_programa():
    return administrativo_distribucion_estudiantes_por_programa_one()

# Servidor Uvicorn para ejecutar directamente con `python main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)