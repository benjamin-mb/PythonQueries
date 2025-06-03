import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#que escuela tiene mas programas
Escuelas_URL="https://cesde-academic-app-development.up.railway.app/escuela/lista"
Escuela_Response=requests.get(Escuelas_URL,auth=HTTPBasicAuth("12344321", "DevUser123"))
data_escuelas=Escuela_Response.json()
df_escuelas=pd.DataFrame(data_escuelas)


Programas_URL="https://cesde-academic-app-development.up.railway.app/programa/lista"
ProgramasResponse=requests.get(Programas_URL,auth=HTTPBasicAuth("12344321", "DevUser123"))
data_Programas=ProgramasResponse.json()
df_programas=pd.DataFrame(data_Programas)

