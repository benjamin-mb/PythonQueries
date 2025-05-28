import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#ser cantidad de clases por modulo y cantidad de horarios por clase en una sola grafica


Modulos_URL="https://cesde-academic-app-development.up.railway.app/modulo/lista"
ModulosResponse=requests.get(Modulos_URL,auth=HTTPBasicAuth("12344321", "DevUser123"))
data_Modulos=ModulosResponse.json()
df_modulos=pd.DataFrame(data_Modulos)

Clases_URL="https://cesde-academic-app-development.up.railway.app/clase/lista"
ClasesResponse=requests.get(Clases_URL,auth=HTTPBasicAuth("12344321", "DevUser123"))
data_Clases=ClasesResponse.json()
df_clases=pd.DataFrame(data_Clases)

ClaseHorario_URL="https://cesde-academic-app-development.up.railway.app/clase-horario/lista"
ClaseHorarios_response=requests.get(ClaseHorario_URL,auth=HTTPBasicAuth("12344321", "DevUser123"))
data_ClaseHorario=ClaseHorarios_response.json()
df_clasesHorarios=pd.DataFrame(data_ClaseHorario)


#cuantas clases tiene un modulo
Clases=df_clases.groupby('modulo').size()
df_clasesPorModulo=Clases.reset_index(name='cantidad de clases por modulo')

#cuantos horarios hay por clase
HorariosClase=df_clasesHorarios.groupby('clase').size()
df_HorariosPorClase=HorariosClase.reset_index(name="cantidad de horarios por clase")

df_HorariosPorClase.rename(columns={'clase': 'modulo'}, inplace=True)

df_comparativo = pd.merge(
    df_clasesPorModulo,
    df_HorariosPorClase,
    on='modulo',
    how='outer'
)

# Ya tenemos el nombre del módulo, así que solo aseguramos que sea string
df_comparativo['modulo'] = df_comparativo['modulo'].astype(str)

df_comparativo.set_index('modulo')[
    ['cantidad de clases por modulo', 'cantidad de horarios por clase']
].plot(kind='barh', figsize=(12, 18))

plt.title('Cantidad de Clases y Horarios por Módulo')
plt.xlabel('Cantidad')
plt.ylabel('Módulo')
plt.tight_layout()
#plt.savefig("guardo la ruta donde guarde la foto de la tabla")
plt.show()
