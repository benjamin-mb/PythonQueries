from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Estudiantes.estudiante_one import analizar_asistencia_estudiante_one

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o especifica tu dominio React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/estudiantes/13/asistencias")
def get_asistencias_13():
    return analizar_asistencia_estudiante_one()