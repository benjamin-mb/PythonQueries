import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import json

#Analítica para calificaciones de una sola clase

estudianteId=13


Calificaciones_URL=f"https://cesde-academic-app-development.up.railway.app/calificacion/estudiante/{estudianteId}"
response=requests.get(Calificaciones_URL)
data_Calificaciones=response.json()
df_calificaciones = pd.DataFrame(data_Calificaciones)

# Verifica si el DataFrame tiene datos
print(df_calificaciones.head())  # <- Agregado para depurar

# Convertir fecha
df_calificaciones['fecha'] = pd.to_datetime(df_calificaciones['fecha'])

# Ordenar por fecha
df_calificaciones = df_calificaciones.sort_values('fecha')

# Crear lista de colores según nota
colors = ['red' if nota < 3 else 'blue' for nota in df_calificaciones['nota']]

# Graficar
plt.figure(figsize=(10, 5))
plt.plot(df_calificaciones['fecha'], df_calificaciones['nota'], color='gray', linestyle='--')
plt.scatter(df_calificaciones['fecha'], df_calificaciones['nota'], color=colors, s=100)
plt.title('Evolución de notas (rojo = reprobado)')
plt.xlabel('Fecha')
plt.ylabel('Nota')
plt.ylim(0, 5)
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()



