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


df = pd.read_csv("respuestas_tokens.tsv", sep="\t")
paid_users = extract_tokens(df)
clean_df(paid_users)


in_colnames = list(paid_users.columns)
print(len(in_colnames))

rename_columns(paid_users, in_colnames, out_colnames)

myjson = paid_users.to_json(orient="records")

with open("users.json", "w", encoding="utf-8") as output_file:
    output_file.write(myjson)
