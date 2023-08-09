#importando las librerias necesarias
from fastapi import FastAPI
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import ast

#definiendo el acceso al repositorio de GitHub
#url_csv = 'https://raw.githubusercontent.com/MayrenS95/PI_MLOPS/main/df_final_movies_.csv'
url_csv = 'https://raw.githubusercontent.com/MayrenS95/PI_MLOPS/main/df_final_movies_.csv'
df_movies_final = pd.read_csv(url_csv)

#instanciando la función
app = FastAPI()

#desarrollando la función de consulta idiomas
@app.get('/peliculas_idioma/{idioma}')
def peliculas_idioma(idioma:str):
    '''Ingresas el idioma, retornando la cantidad de peliculas producidas en el mismo'''

#filtrando los valores del df a través de una mascara
    respuesta = df_movies_final['original_language'][df_movies_final['original_language']==idioma]

    return {'idioma':idioma, 'cantidad':respuesta.shape[0]}


#Definiendo la funciòn de pelicula
@app.get('/peliculas_duracion/{pelicula}')
def peliculas_duracion(pelicula:str):
    '''Ingresas la pelicula, retornando la duracion y el año'''

    respuesta = list(df_movies_final['runtime'][df_movies_final['title']==pelicula])
    anio = list(df_movies_final['Year'][df_movies_final['title']==pelicula])

    return {'pelicula':pelicula, 'duracion':respuesta, 'anio':anio}


#definiendo la función consulta franquicia

@app.get('/franquicia/{franquicia}')
def franquicia(franquicia:str):
    '''Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio'''

    respuesta = df_movies_final['title'][df_movies_final['name_belongs'].str.lstrip()==franquicia].shape[0]
    r_gananciat = (df_movies_final['revenue']-df_movies_final['budget'])[df_movies_final['name_belongs'].str.lstrip()==franquicia].sum().round(2)
    r_gananciap = (df_movies_final['revenue']-df_movies_final['budget'])[df_movies_final['name_belongs'].str.lstrip()==franquicia].mean().round(2)


    return {'franquicia':franquicia, 'cantidad':respuesta, 'ganancia_total':r_gananciat, 'ganancia_promedio':r_gananciap
            }


#definiendo la función de pais de producción
@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais:str):
    '''Ingresas el pais, retornando la cantidad de peliculas producidas en el mismo'''

    respuesta = 0
    df = df_movies_final['production_countries'].apply(ast.literal_eval)
    for i in df:
        for n in i:
            if n.lstrip() == pais:
                respuesta += 1

    return {'pais':pais, 'cantidad':respuesta}


#definiendo la funcion de compañias productoras exitosas, con el revenue
@app.get('/productoras_exitosas/{productora}')
def productoras_exitosas(productora:str):
    '''Ingresas la productora, entregandote el revenue total y la cantidad de peliculas que realizo '''

    cantidad = 0
    revenue_total = 0
    df = df_movies_final['production_companies'].apply(ast.literal_eval)
    for i in range(len(df)):
        for n in df[i]:
            if n == productora:
                revenue_total += df_movies_final['revenue'][i]
                cantidad += 1
    

    return {'productora':productora, 'revenue_total': revenue_total, 'cantidad':cantidad}

#definiendo la funcion de director
@app.get('/get_director/{nombre_director}')
def get_director(nombre_director:str):
    ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma. En formato lista'''
    
    #cambiando el valor de los nulos
    df_movies_final['name'].fillna("['nada']", inplace=True)

    #retorno total
    df = df_movies_final['name'].apply(ast.literal_eval)
    revenue= 0
    budget=0
    revenue_total=0
    for i in range(len(df)):
        for n in df[i]:
            if n == nombre_director:
                revenue= revenue + df_movies_final['revenue'][i]
                budget= budget + df_movies_final['budget'][i]
                revenue_total= (revenue - budget) / budget


    #peliculas
    
    lista_peliculas = []
    for i in range(len(df)):
        for n in df[i]:
            if n == nombre_director:
                lista_peliculas.append(df_movies_final['title'][i])

    #anio
    lista_anio = []
    for i in range(len(df)):
        for n in df[i]:
            if n == nombre_director:
                lista_anio.append(df_movies_final['Year'][i].item())

    #revenue, budget y retorno pelicula total 
    lista_revenue= []
    lista_budget= []
    revenue_total_peli= []
    for i in range(len(df)):
        for n in df[i]:
            if n == nombre_director:
                lista_revenue.append(df_movies_final['revenue'][i])
                lista_budget.append(df_movies_final['budget'][i])
                revenue_total_peli.append(df_movies_final['return'][i])

    
    return {'director':nombre_director, 'retorno_total_director':revenue_total, 
    'peliculas':lista_peliculas, 'anio':lista_anio , 'retorno_pelicula':revenue_total_peli, 
    'budget_pelicula':lista_budget, 'revenue_pelicula':lista_revenue
            }
        

#ML --- Sistema de recomendación
@app.get('/recomendacion/{titulo}')
def recomendacion(titulo:str):
    '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''
    #se define una cantidad especifica a usar del dataset por razones de rendimiento del equipo
    df = df_movies_final.loc[0:4000]

    #se importan librerias para usar la función tf - idf vector
    from sklearn.feature_extraction.text import TfidfVectorizer

    #se instancia la función, pasando las palabras a omitir en una lista 
    tfidf = TfidfVectorizer(stop_words='english')

    #se sustituyen los nulos en la columna a usar para el sistema de recomendación
    df['genres'] = df['genres'].fillna('')

    #se trasnforman los datos de la columna a usar en matriz
    tfidf_matrix = tfidf.fit_transform(df['genres'])

    #se importa la libreria para usar la funcion del coseno
    from sklearn.metrics.pairwise import linear_kernel

    #se calcula el coseno con la multiplicación de las matrices
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    #se establece los indices de la etiqueta a generar
    indices = pd.Series(df.index, index=df['title']).drop_duplicates()

    #se establece la función que llevará a cabo los cálculos automaticamente
    def recomendation(title, cosine_sim=cosine_sim):
        
        idx = indices[title]

        sim_scores = list(enumerate(cosine_sim[idx]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        sim_scores = sim_scores[1:6]

        movie_indices = [i[0] for i in sim_scores]

        return df['title'].iloc[movie_indices]
    
    respuesta = recomendation(titulo)
    return {'lista recomendada': respuesta}
