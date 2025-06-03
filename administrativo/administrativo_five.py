import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#promedio de notas por clase

Clases_URL="https://cesde-academic-app-development.up.railway.app/clase/lista"
response_clase=requests.get(Clases_URL,auth=HTTPBasicAuth("12344321", "DevUser123"))
data_clases=response_clase.json()
df_clases=pd.DataFrame(data_clases)

Calificaiones_URL="https://cesde-academic-app-development.up.railway.app/calificacion/lista"
response_calificaciones=requests.get(Calificaiones_URL,auth=HTTPBasicAuth("12344321", "DevUser123"))
data_calificaciones=response_calificaciones.json()
df_calificaciones=pd.DataFrame(data_calificaciones)

Actividades_URL="https://cesde-academic-app-development.up.railway.app/actividad/lista"
response_actividades=requests.get(Actividades_URL,auth=HTTPBasicAuth("12344321", "DevUser123"))
data_actividades=response_actividades.json()
df_actividades=pd.DataFrame(data_actividades)

# Paso 1: renombramos columnas para facilitar el merge
df_actividades_ren = df_actividades.rename(columns={
    "tipo": "actividad", 
    "fechaEntrega": "fecha"
})

# Paso 2: combinamos por 'actividad' y 'fecha'
df_notas_con_actividad = pd.merge(
    df_calificaciones,
    df_actividades_ren,
    on=["actividad", "fecha"],
    how="left"
)

#extraemos de el diccionea
df_notas_con_actividad["grupo"] = df_notas_con_actividad["clase"].apply(lambda c: c["grupo"])

df_notas_con_clase = df_notas_con_actividad.merge(df_clases, on="grupo", how="left")
df_promedio_por_clase = df_notas_con_clase.groupby("id")["nota"].mean().reset_index()
print(df_promedio_por_clase)


def color_por_nota(nota):
    if nota < 3.0:
        return 'red'
    elif nota < 4.0:
        return 'gold'
    else:
        return 'green'

# Aplicar colores
colores = df_promedio_por_clase["nota"].apply(color_por_nota)

# Crear figura más ancha para todos los IDs
plt.figure(figsize=(max(12, len(df_promedio_por_clase) * 0.5), 6))

# Dibujar barras con color y borde
plt.bar(df_promedio_por_clase["id"], df_promedio_por_clase["nota"],
        color=colores, edgecolor='black', width=0.6)

# Título y ejes
plt.title("Promedio de Nota por Clase (Todos los IDs Visibles)", fontsize=14)
plt.xlabel("ID de Clase")
plt.ylabel("Promedio de Nota")

# Mostrar todos los ticks de ID en el eje X
plt.xticks(
    ticks=df_promedio_por_clase["id"],
    labels=df_promedio_por_clase["id"],
    rotation=90,
    fontsize=8  # Tamaño pequeño para que quepan
)

# Mostrar el valor numérico encima de cada barra
for i, v in enumerate(df_promedio_por_clase["nota"]):
    plt.text(df_promedio_por_clase["id"].iloc[i], v + 0.03, f"{v:.2f}",
             ha='center', va='bottom', fontsize=7)

plt.tight_layout()
plt.show()
