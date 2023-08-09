<center><img src="logo henry.PNG" alt="logo henry"></center>
<h1><strong><center>--------PROYECTO INDIVIDUAL I-------<center></strong></h1>

<h2 style="color:pink"><strong><center>Machine Learning Operations (MLOps)<center></strong></h1>

<h3 style="color:gray">DATASET: MOVIES</h3>

<p style="text-align: justify">Primero se comienza con la revisión del dataset movies, donde se evidencia que existen columnas con valores anidados que deben de ser separados para tener una mejor visualización de los mismos.</p>

<p style="text-align: justify">Se evidencia que la columna 'bellongs_to_collection', 'production_companies','production_countries','spoken_languages', 'genres' son unas de las candidatas a ser trabajadas y por tanto, se define trabajarla por separado del dataset original.</p>

<ol start="1.">
    <li>se procede a cambiar el tipo de dato a string,</li>
<li>se hace uso de la función split (propio de cadenas) para separar el texto en columnas, este texto está delimitado por ','</li>
<li>se procede a renombrar las columnas obtenidas, haciendo uso del metodo replace se procede a limpiar el dato,</li>
<li>posteriormente se procede a eliminar las columnas que no son necesarias del dataframe en el que esta trabajando por separado,</li>
<li>se procede a realizar la unión con el dataset original,</li>
<li>* para el caso de columnas como production_companies, genres, spoken_languages,'production_countries', se procede a convertir el valor de cad registro en una lista,</li>
<li>* En el caso de 'production countries' y 'spoken_languages' se realiza un proceso de iteraciòn paraseleccionar solo las iniciales del paìs y trabajar con estos valores.</li>


<p style="text-align: justify"> Nota: Se debe tener en cuenta que para cada columna trabajada por separado y obtenido ya el resultado final, se deben de eliminar del dataset original para evitar duplicidad.</p>

<li>Posteriormente se procede a realizar un reemplazo de los valores nulos por 0  contenidos en la columna 'revenue' y 'budget',</li>

<li>Teniendo en cuenta que los valores nulos del campo 'release_date' deben de ser eliminados,</li>

<li>Se valida el formato fecha de la columna 'release_date', haciendo uso del largo del texto para identificar aquellos registros que no poseen la cantidad minima necesaria para ser considerados en el analisis</li>

<li>Posteriormente se le da el formato como fecha a travès de la aplicación de la función lambda,</li>

<li>Se procede a insertar la columna con año en dataset,</li>

<li>Se calcula la columna return = revenue / budget, reemplazando valores nulos e inf,</li>

<li>Se procede a eliminar las columnas que no serán utilizadas como 'video, imdb_id, audlt,original_title, poster_path, homepage,</li>
</ol>

<h3 style="color:gray">DATASET: CREDITS</h3>

<p style="text-align: justify">Teniendo en cuenta que de este bloque de datos solo se necesita la información de los directores de las películas, se procede a hacer uso de la función as.literal_eval para convertirlos en tipo lista 
y separar luego los contenidos en las columnas job y name a través del metodo explode.</p>

<ol start="1.">

<li>Se procede a filtrar solo los registros = Director en la columna job.</li>

<li>Se procede a convertir todo en lista haciendo uso del metodo apply y la funcion lambda,</li>

<li>Posteriormente se unen los dataframes Movies y Credits (resultante)</li>

<li>Se genera el dataset limpio para ser empleado en los analisis posteriores.</li>
</ol>
<hr style="color: Black">

<h3 style="color:pink"><center>#MACHINE LEARNING</center></h3>

<ol start="1.">

<li>Se hace uso de las librerias necesarias para realizar el analisis</li>
<li>Se procede a ver una breve descripción estadñistica de los datos, tanto cualitativos como cuantitativos, lo que nos permite tener una idea de la distribución de los mismos,</li>
<li>Se realiza un mapa de calor o heatmap para evidenciar que columnas tienen valores nulos,</li>
<li>Se realiza el calculo de correlación de las variables númericas, graficandolo a tarves de un mapa de calor,</li>
<li>Se genera nube de palabras para una de las variables cualitativas como lo es genres = genero,</li>

<p style="text-align: center">* Se procede a realizar el sistema de recomendación, en este caso se hará uso de la columna genres, por permitir caracterizar las películas y ser una de las columnas con mejor completitud en cuanto a datos.</p>

<p style="text-align: justify">Se hara uso de la función Tf e IDF vector, que nos permite clasificar documentos, a través de ciertos cálculos matemáticos.</p>

<ol strat="1." style="padding-left:0 ;">

<li>se instancia la función y se pasa al argumento de la misma una lista de palabras a omitir para su analisis,</li>
<li>se sutoituyen los valoers nulos de la columna a trabajar, genres,</li>
<li>Se procede a transformar los datos de la columna genres,</li>
<li>se hace uso de la funcion linear_kernel, la cual relaiza una comparación entre las matrices del argumento,</li>
<li>se calculan los indices de la etiqueta o valor resultante que esperamos del analisis y eliminamos duplicados,</li>
<li>definimos la función que hará todo el sistema de recomendación y recibira el título  de la película y el calor del conseno calculado a través de linear_kernel</li>
<li>se realiza la prueba del sistema de recomendación con la función definida,</li>
</ol>
<hr style="color: Black">

<h3 style="color:pink"><center>REPOSITORIO GIT HUB</center></h3>

<p>Repostirorio Proyecto : <a>https://github.com/MayrenS95/PI_MLOPS.git</a></p>

<p>Se carga el dataset resultante en git, con el siguiente enlace:</p>

<p style="color:pink"><center>url_csv = <a>'https://raw.githubusercontent.com/MayrenS95/PI_MLOPS/main/df_final_movies_.csv'</a></center></p>

<hr style="color: Black">

<h3 style="color:pink"><center>API - FASTAPI</center></h3>
<ol strat="1." style="padding-left:0 ;">

<li>Se procede a crear API para ser consumida a través de la web,</li>
<li>Establecienod la configuración necesaria de librerñia uvicorn y levantamiento de la misma,</li>
<li>Se hace consumo del dataset resultante alojado en git hub,</li>
<li>Se establecen las funciones de la información solicitada por parte de este proyecto como se describe a continuación:</li>
</ol>
@app.get('/peliculas_idioma/{idioma}')
def peliculas_idioma(idioma:str):
    '''Ingresas el idioma, retornando la cantidad de peliculas producidas en el mismo'''
    return {'idioma':idioma, 'cantidad':respuesta}
    
 @app.get('/peliculas_duracion/{pelicula}')
def peliculas_duracion(pelicula:str):
    '''Ingresas la pelicula, retornando la duracion y el año'''
    return {'pelicula':pelicula, 'duracion':respuesta, 'anio':anio}



@app.get('/franquicia/{franquicia}')
def franquicia(franquicia:str):
    '''Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio'''
    return {'franquicia':franquicia, 'cantidad':respuesta, 'ganancia_total':respuesta, 'ganancia_promedio':respuesta}

@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais:str):
    '''Ingresas el pais, retornando la cantidad de peliculas producidas en el mismo'''
    return {'pais':pais, 'cantidad':respuesta}

@app.get('/productoras_exitosas/{productora}')
def productoras_exitosas(productora:str):
    '''Ingresas la productora, entregandote el revunue total y la cantidad de peliculas que realizo '''
    return {'productora':productora, 'revenue_total': respuesta,'cantidad':respuesta}


@app.get('/get_director/{nombre_director}')
def get_director(nombre_director:str):
    ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma. En formato lista'''
    return {'director':nombre_director, 'retorno_total_director':respuesta, 
    'peliculas':respuesta, 'anio':respuesta,, 'retorno_pelicula':respuesta, 
    'budget_pelicula':respuesta, 'revenue_pelicula':respuesta}

<hr style="color: Black">

<h3 style="color:pink"><center>MACHINE LEARNING</center></h3>


@app.get('/recomendacion/{titulo}')
def recomendacion(titulo:str):
    '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''
    return {'lista recomendada': respuesta}


<p>Se procede a activar la misma en la terminal a través del comando: python -m uvicorn main:app --reload</p>

<p>Teniendo como url de acceso: <a>http://127.0.0.1:8000/</a></p>

<hr style="color: Black">

<h3 style="color:pink"><center>RENDER</center></h3>

<ol start="1." style="padding-left:0 ;" >

<li>Se procede a enlazar todo el repositorio de git hub donde se encuentra la totalidad del proyecto con render, que nos permite tener acceso a esta API a través de la web</li>

<li>Para la realización se debe crear una cuenta en Render, gratuita y proceder a hacer click en sahboards, nuevo web service,</li> 

<li>Se completan las casillas con la información descrita en: <a>https://github.com/HX-FNegrete/render-fastapi-tutorial.git </a></li>

<li>El sistema de render comenzará a levantar el proceso e indicará los pasos posteriores o si hace flata algo por instalar en cuanto a versiones,</li>

<li>Posteriormente estara creado el servicio a través del siguiente enlace: <a>https://pimlops-mayren.onrender.com/docs</a></li>
</ol>