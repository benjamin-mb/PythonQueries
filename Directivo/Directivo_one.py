import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


#cuantos programas hay por escuela

Escuelas_URL="https://cesde-academic-app-development.up.railway.app/escuela/lista"
Escuelas_response=requests.get(Escuelas_URL,auth=HTTPBasicAuth("12344321", "DevUser123"))
data_Escuelas=Escuelas_response.json()
df_escuelas=pd.DataFrame(data_Escuelas)

Programas_URL="https://cesde-academic-app-development.up.railway.app/programa/lista"
ProgramasResponse=requests.get(Programas_URL,auth=HTTPBasicAuth("12344321", "DevUser123"))
data_Programas=ProgramasResponse.json()
df_programas=pd.DataFrame(data_Programas)

escuelasPrograma=df_programas.groupby('escuela').size()
escuelasPrograma_df = escuelasPrograma.reset_index(name='cantidad_programas')

sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.barplot(
    data=escuelasPrograma_df.sort_values('cantidad_programas', ascending=True),
    x='cantidad_programas',
    y='escuela',
    palette='viridis'
)
plt.title("Cantidad de Programas por Escuela")
plt.xlabel("Número de Programas")
plt.ylabel("Escuela")
plt.tight_layout()
plt.show()