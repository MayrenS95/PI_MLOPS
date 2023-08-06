#importando las librerias necesarias
from fastapi import FastAPI
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import ast

#url_csv = 'https://raw.githubusercontent.com/MayrenS95/PI_MLOPS/main/df_final_movies_.csv'
url_csv = 'https://raw.githubusercontent.com/MayrenS95/PI_MLOPS/main/df_final_movies_.csv'
df_movies_final = pd.read_csv(url_csv)

app = FastAPI()


@app.get('/peliculas_idioma/{idioma}')
def peliculas_idioma(idioma:str):
    '''Ingresas el idioma, retornando la cantidad de peliculas producidas en el mismo'''

    respuesta = df_movies_final['original_language'][df_movies_final['original_language']==idioma]

    return {'idioma':idioma, 'cantidad':respuesta.shape[0]}


    
@app.get('/peliculas_duracion/{pelicula}')
def peliculas_duracion(pelicula:str):
    '''Ingresas la pelicula, retornando la duracion y el año'''

    respuesta = list(df_movies_final['runtime'][df_movies_final['title']==pelicula])
    anio = list(df_movies_final['Year'][df_movies_final['title']==pelicula])

    return {'pelicula':pelicula, 'duracion':respuesta, 'anio':anio}



@app.get('/franquicia/{franquicia}')
def franquicia(franquicia:str):
    '''Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio'''

    respuesta = df_movies_final['title'][df_movies_final['name_belongs'].str.lstrip()==franquicia].shape[0]
    r_gananciat = (df_movies_final['revenue']-df_movies_final['budget'])[df_movies_final['name_belongs'].str.lstrip()==franquicia].sum().round(2)
    r_gananciap = (df_movies_final['revenue']-df_movies_final['budget'])[df_movies_final['name_belongs'].str.lstrip()==franquicia].mean().round(2)


    return {'franquicia':franquicia, 'cantidad':respuesta, 'ganancia_total':r_gananciat, 'ganancia_promedio':r_gananciap
            }



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
        