import pandas as pd
import json
import csv

out_colnames = [
    "orientacion",
    "genero",
    "telefono",
    "mascota",
    "signo",
    "entretenimiento",
    "pasatiempo",
    "personalidad",
    "peliculas",
    "comida",
    "loteria",
    "bebida",
    "b_alcoholica",
    "viaje",
    "musica",
    "prioridad_pareja",
    "terapia",
    "nombre",
]

json_data = []

print(len(out_colnames))


# extract pais users
def extract_tokens(df):
    out = df.dropna()
    return out


# remove unused columns


def clean_df(df):
    del df["Marca temporal"]
    del df["Token"]
    return df


# rename columns
def rename_columns(df, in_colnames, out_colnames):
    n = len(in_colnames)
    for i in range(n):
        df.rename(columns={in_colnames[i]: out_colnames[i]}, inplace=True)

# compara 2 personas, en un csv especifico
def get_valor_pregunta(numPregunta,p1,p2,key):
    total=0
    concatenate_string  = 'Pregunta' + str(numPregunta) + '.tsv'
    df = pd.read_csv(concatenate_string, index_col='col_name', sep="\t")
    total=df.loc[[p1[key]],[p2[key]]].squeeze()
    return total

# calucla el indice total entre 2 personas
def calcular_indice(p1,p2):
    indice=0
    counter=1
    if relacion_entre_interesados(p1,p2) == True:
      for i in range(3,16):
          #print(get_valor_pregunta(counter,p1,p2,lista_keys[i]))
          indice += get_valor_pregunta(counter,p1,p2,lista_keys[i])
          counter+=1
    return indice

#no tiene que tomar en cuenta, si los ponemos con 0, tarda mucho el sistema
def relacion_entre_interesados(p1,p2):
  op1 = p1["orientacion"] #op = orientacion persona
  gp1 = p1["genero"]      #gp = genero persona
  op2 = p2["orientacion"]
  gp2 = p2["genero"]
  if(op1 == "Homosexual" or op1 == "Bisexual"):
    if(gp1 == gp2 and (op2 == "Homosexual" or op2 == "Bisexual")):
      return True
  
  if(op1 == "Heterosexual" or op1 == "Bisexual"):
     if(gp1 != gp2 and (op2 == "Heterosexual" or op2 == "Bisexual")):
      return True

  return False


def usar_algoritmo_con_una_persona(p1):
  dictionary = {}
  res=0
  for persona in json_data:
    if(persona["nombre"] != p1["nombre"]):
      res=calcular_indice(p1,persona)
      #print(persona["nombre"], "/", p1["nombre"])
    
    dictionary[persona["nombre"]] = []
    dictionary[persona["nombre"]] = res
    res=0

  return dict(dictionary.items())

def lista_maximos_scores(json_data):
    dictionary={}
    for persona in json_data:
        dictionary[persona["nombre"]] = []
        dictionary[persona["nombre"]] = usar_algoritmo_con_una_persona(persona)
    return dictionary

def sacar_pareja(nombre_persona1,df):  
    df_especial=df
    lista_valores=list(df[nombre_persona1].array)
    maximo=max(list(df[nombre_persona1]))
    indice=df.loc[df[nombre_persona1] == maximo].index.array[0]
    indice_max=df[indice].max()
    while(maximo!=indice_max):
        df_especial=df_especial.drop(columns=[indice])
        df_especial=df_especial.drop(indice)
        lista_valores.remove(maximo)
        aux=max(lista_valores)
        maximo=aux
        indice=df_especial.loc[df_especial[nombre_persona1] == maximo].index.array[0]
        indice_max=df_especial[indice].max()
    pareja=[nombre_persona1,indice,indice_max]
    return pareja

def lista_parejas(df):
    lista_parejas=[]
    for i in df:
        lista_parejas.append(sacar_pareja(i,df))
    return lista_parejas

def limpiar_max_df(df,parejitas):
    for elemento in parejitas:
        if(elemento[2]!=0):
            df=df.drop(columns=[elemento[0]])
            df=df.drop(elemento[0])
    return df

def buscar_json(elemento):
    for i in json_data:
        if (i["nombre"] == elemento[0]):
            tel1 = i["telefono"]
        if (i["nombre"] == elemento[1]):
            tel2 =  i["telefono"]
    data = [elemento[0],tel1, elemento[1],tel2,elemento[2]]
    return data

def parejas_a_csv(parejas):
    for elemento in parejas:
        if(elemento[2]!=0):
            datos = buscar_json(elemento)
            with open('parejas.csv', 'a', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(datos)
                f.close()

def assign_header():
    header =["nombre1", "telefono1","nombre2","telefono2","indice compatibilidad"]
    with open('parejas.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
                
def delete_data_csv():
    with open('parejas.csv', 'w', encoding='UTF8', newline='') as f:
        f.truncate()
        f.close()


def parejas_final(df):
    delete_data_csv()
    assign_header()
    prev_df=pd.DataFrame
    while(df.size != prev_df.size):
        prev_df = df
        parejas = lista_parejas(df)
        parejas_a_csv(parejas)
        df = limpiar_max_df(df,parejas)   

df = pd.read_csv("respuestas_tokens.tsv", sep="\t")

paid_users = extract_tokens(df)

df = clean_df(paid_users)

in_colnames = list(df.columns)

rename_columns(df, in_colnames, out_colnames)

myjson = df.to_json(orient="records")

with open("users.json", "w", encoding="utf-8") as output_file:
    output_file.write(myjson)

with open('users.json') as json_file:
   json_data = json.load(json_file)
   
lista_keys=list(json_data[0].keys())

lista_completa = lista_maximos_scores(json_data)
df_indice_relacion = pd.DataFrame.from_dict(lista_completa, orient='index')

parejas_final(df_indice_relacion)