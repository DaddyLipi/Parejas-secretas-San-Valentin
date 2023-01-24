import pandas as pd
import json

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
    for i in range(3,16):
        print(get_valor_pregunta(counter,p1,p2,lista_keys[i]))
        indice += get_valor_pregunta(counter,p1,p2,lista_keys[i])
        counter+=1
    return indice


df = pd.read_csv("respuestas_tokens.tsv", sep="\t")
paid_users = extract_tokens(df)
clean_df(paid_users)


in_colnames = list(paid_users.columns)
print(len(in_colnames))

rename_columns(paid_users, in_colnames, out_colnames)

myjson = paid_users.to_json(orient="records")

with open("users.json", "w", encoding="utf-8") as output_file:
    output_file.write(myjson)

with open('users.json') as json_file:
   json_data = json.load(json_file)
   

lista_keys=list(json_data[0].keys())