import numpy as np
import pandas as pd
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import nltk
import datetime as dt

nltk.download("movie_reviews")
nltk.download("punkt")

movie = pd.read_csv("tmdb_5000_movies.csv")
credit = pd.read_csv("tmdb_5000_credits.csv")

print(movie.isnull().sum())
print('Duplicados')
print(movie.duplicated().sum())

print(credit.isnull().sum())
print('Duplicados')
credit.duplicated().sum()

df_movies = movie.merge(credit, left_on='id', right_on='movie_id')

df_movies.head()

df_movies.drop(['title_y', 'movie_id', 'spoken_languages', 'status', 'title_x'],
               axis=1, inplace=True)

df_movies.columns

df_movies.columns = ['presupuesto', 'generos', 'homepage', 'id', 'keywords', 'idioma', 'titulo', 'sinopsis', 'popularidad',
                     'productora', 'pais', 'fecha', 'recaudacion', 'duracion', 'tagline', 'rate',
                     'rate_count', 'cast', 'director']

df_movies['sinopsis'][0]

df_movies.iloc[0, 1]

import ast

ast.literal_eval('[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"},'
                 '{"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]')


def clean(text):
    x = []
    for i in ast.literal_eval(text):
        x.append(i['name'])
    y = x[:]
    return y


df_movies['generos'] = df_movies['generos'].apply(clean)
df_movies['productora'] = df_movies['productora'].apply(clean)
df_movies['pais'] = df_movies['pais'].apply(clean)
df_movies




def reducir_cast(text):
    x = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter == 3:
            break
        x.append(i['name'])
        counter += 1

    y = x[:]
    return y


df_movies['cast'] = df_movies['cast'].apply(reducir_cast)
df_movies


def buscar_director(text):
    x = []
    for i in ast.literal_eval(text):
        if i['job'] == "Director":
            x.append(i['name'])
    y = x[:]
    return y


df_movies['director'] = df_movies['director'].apply(buscar_director)

df_movies.dropna(subset=['sinopsis'], inplace=True)

df_movies['sinopsis'] = df_movies['sinopsis'].apply(lambda x: x.split())

df_movies['sinopsis']


def keyword(text):
    x = []
    for i in ast.literal_eval(text):
        x.append(i['name'])
    y = x[:]
    return y


df_movies['keywords'] = df_movies['keywords'].apply(keyword)


def limpiar_espacios(lista):
    x = []
    for i in lista:
        x.append(i.replace(" ", ""))
    y = x[:]
    return y


df_movies['generos'] = df_movies['generos'].apply(limpiar_espacios)
df_movies['cast'] = df_movies['cast'].apply(limpiar_espacios)
df_movies['director'] = df_movies['director'].apply(limpiar_espacios)
df_movies['sinopsis'] = df_movies['sinopsis'].apply(limpiar_espacios)

df_movies['datos'] = df_movies['generos'] + df_movies['cast'] + df_movies['director'] + df_movies['sinopsis']

df_palabras1 = df_movies[['titulo', 'datos', 'fecha', 'duracion',
                          'rate', 'rate_count', 'sinopsis','generos', 'homepage']]
df_palabras1['fecha'] = pd.to_datetime(df_palabras1['fecha'])

df_palabras1['fecha'] = df_palabras1['fecha'].dt.year


def time(data):
    if data >= 150:
        return ("Más de 2h30")
    elif (data >= 120) and (data < 150):
        return ("Entre 2h y 2h30")
    elif (data >= 90) and (data < 120):
        return ("Entre 1h30 y 2h")
    else:
        return ("Menos de 1h30")


df_palabras1['duracion'] = df_palabras1['duracion'].apply(time)


def rate(data):
    if data >= 7:
        return ("Buena")
    else:
        return ("Mala")


df_palabras1['rate'] = df_palabras1['rate'].apply(rate)


def pop(data):
    if data >= 733:
        return ("Popular")
    else:
        return ("No popular")


df_palabras1['rate_count'] = df_palabras1['rate_count'].apply(pop)


def sacarcorchetes(lista):
    str = " "
    return (str.join(lista))


df_palabras1['datos'] = df_palabras1['datos'].apply(sacarcorchetes)
df_palabras1['datos'] = df_palabras1['datos'].apply(lambda x: x.lower())
df_palabras1['sinopsis'] = df_palabras1['sinopsis'].apply(sacarcorchetes)
df_palabras1['sinopsis'] = df_palabras1['sinopsis'].apply(lambda x: x.lower())
df_palabras1['generos'] = df_palabras1['generos'].apply(sacarcorchetes)
df_palabras1['generos'] = df_palabras1['generos'].apply(lambda x: x.lower())


import pickle


with open('pelisok.pkl', 'rb') as pelisok:
    pelisok = pickle.load(pelisok)

df_palabras1 = pelisok