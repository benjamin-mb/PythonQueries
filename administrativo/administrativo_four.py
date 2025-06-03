import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

ClasesHorarios_URL="https://cesde-academic-app-development.up.railway.app/clase-horario/lista"
response_ClaseHorario=requests.get(ClasesHorarios_URL,auth=HTTPBasicAuth("12344321", "DevUser123"))
data_claseHorario=response_ClaseHorario.json()
df_claseHorarios=pd.DataFrame(data_claseHorario)

#print(df_claseHorarios)

conteo_dias = df_claseHorarios.groupby('dia').size().reindex(
    ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO'],
    fill_value=0
)

conteo_dias.plot(kind='bar', figsize=(10,5), color='skyblue', edgecolor='black')
plt.title("Número de clases por día de la semana")
plt.xlabel("Día")
plt.ylabel("Cantidad")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
