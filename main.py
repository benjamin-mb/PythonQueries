from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Estudiantes.estudiante_one import analizar_asistencia_estudiante_13

app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto si tienes un frontend específico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta para obtener asistencia del estudiante 13
@app.get("/estudiantes/13/asistencias")
def get_asistencias_13():
    return analizar_asistencia_estudiante_13()

# Servidor Uvicorn para ejecutar directamente con `python main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
