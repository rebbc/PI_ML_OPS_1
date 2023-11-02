
from fastapi import FastAPI
import pandas as pd


df_usersrecommend = pd.read_csv('datasets/df_usersrecommend.csv')
df_playtime = pd.read_csv('datasets/df_playtimegenre.csv')
df_ml = pd.read_csv('datasets/df_ml.csv')
df_ml_names = pd.read_csv('datasets/df_ml_names.csv')

app = FastAPI()

@app.get("/sentiment_analysis/{ano}")

async def sentiment_analysis(ano:int):
    
    year = df_usersrecommend[df_usersrecommend['posted_year'] == ano]
    sentiment_counts = year['sentiment_analysis'].value_counts()
    cant_negativo = sentiment_counts.get(0)
    cant_neutral = sentiment_counts.get(1)
    cant_positivo = sentiment_counts.get(2)
    result = {
            f"Negativo: {cant_negativo}, Neutral: {cant_neutral}, Positivo: {cant_positivo}"   
        }
    
    return result




@app.get("/usersnotrecommend/{ano}")

async def UsersNotRecommend(ano:int):

    year_review = df_usersrecommend[df_usersrecommend['posted_year'] == ano]


    reviews_recommend = year_review[year_review['recommend'] == False] 

    sentiment_analysis_pos = reviews_recommend[reviews_recommend['sentiment_analysis'].isin([0])]

    review_games_pos = sentiment_analysis_pos['item_id'].value_counts()
    review_games_pos = review_games_pos.sort_values(ascending=False) #sigue siendo False porque son los que tienen mas reacciones negativas

    top_3 = review_games_pos.head(3)
    if top_3.empty:
        error = f"No se encontraron juegos recomendados para el año especificado."
        return error
    
    top_3_nombres = df_usersrecommend[df_usersrecommend['item_id'].isin(top_3.index)][['item_id', 'item_name']].value_counts()

    puesto1 = top_3_nombres.index[0][1]
    puesto2 = top_3_nombres.index[1][1]
    puesto3 = top_3_nombres.index[2][1]

    resultado = {
        f"Puesto 1:, {puesto1}, Puesto 2: {puesto2}, Puesto 3: {puesto3}"
    }

    return resultado


@app.get("/usersrecommend/{ano}")

async def UsersRecommend(ano:int): 
    
    year_review = df_usersrecommend[df_usersrecommend['posted_year'] == ano]


    reviews_recommend = year_review[year_review['recommend'] == True] 

    sentiment_analysis_pos = reviews_recommend[reviews_recommend['sentiment_analysis'].isin([1, 2])]

    review_games_pos = sentiment_analysis_pos['item_id'].value_counts()
    review_games_pos = review_games_pos.sort_values(ascending=False)

    top_3 = review_games_pos.head(3)
    if top_3.empty:
        error = f"No se encontraron juegos recomendados para el año especificado."
        return error
    
    top_3_nombres = df_usersrecommend[df_usersrecommend['item_id'].isin(top_3.index)][['item_id', 'item_name']].value_counts()

    puesto1 = top_3_nombres.index[0][1]
    puesto2 = top_3_nombres.index[1][1]
    puesto3 = top_3_nombres.index[2][1]

    resultado = {
        f"Puesto 1:, {puesto1}, Puesto 2: {puesto2}, Puesto 3: {puesto3}"
    }

    return resultado

@app.get("/playtimegenre/{genero}")

async def PlayTimeGenre(genero:str): 

    data_genero = df_playtime[df_playtime['genres'] == genero]
    
    group = data_genero.groupby('posted_year')['playtime_forever'].sum()
    max_anio = group.idxmax(skipna=True)

    result = {f"Año de lanzamiento con más horas jugadas para {genero}: {max_anio}"}

    return result

@app.get("/userforgenre/{genero}")

async def UserForGenre(genero:str):
    
    data_genero = df_playtime[df_playtime['genres'] == genero]    
    group = data_genero.groupby('user_id')['playtime_forever'].sum()
    usuario_max_hs = group.idxmax()
    data_usuario_max_hs = data_genero[data_genero['user_id'] == usuario_max_hs]
    horas_por_ano = data_usuario_max_hs.groupby('posted_year')['playtime_forever'].sum()

    acumulacion_horas = [{"Año": int(year), "Horas": int(horas)} for year, horas in horas_por_ano.items()]

    resultado = {
        "Usuario con más horas jugadas para " + genero: usuario_max_hs,
        "Horas jugadas": acumulacion_horas
    }

    return resultado



@app.post("/recomendacion_usuario/")

async def recomendacion_usuario(user_id:int):
    
    if user_id not in df_ml['user_id'].values:
        return f"El usuario {user_id} no se encuentra."

    user_cluster = df_ml[df_ml['user_id'] == user_id]['cluster'].values[0]

    users_mismo_cluster = df_ml[df_ml['cluster'] == user_cluster]

    juegos_recomendados = users_mismo_cluster.groupby('item_id')['recommend'].sum()
    
    top_5 = juegos_recomendados.sort_values(ascending=False).head(5)
    

    recomendaciones = []
    for i, game_id in enumerate(top_5.index):
        game_name = df_ml_names.loc[df_ml_names['item_id'] == game_id, 'item_name'].values
        recomendaciones.append(f"Recomendación {i+1}: {game_name[0]}")
    respuesta = {"Recomendaciones para el usuario": user_id, "recomendaciones": recomendaciones}
    return respuesta
