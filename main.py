from fastapi import FastAPI
import pandas as pd

df_steams = pd.read_csv('datasets/data_outputs.csv') 
df_review = pd.read_csv('datasets/data_user.csv')


app = FastAPI()

@app.get("/sentiment_analysis/{ano}")

async def sentiment_analysis(ano:int): 

    release_year = df_steams[df_steams['release_year'] == ano]
    merged_data = release_year.merge(df_review, on='item_id', how='inner')

    sentiment_counts = merged_data['sentiment_analysis'].value_counts()
    
    cant_negativo = sentiment_counts.get(0)
    cant_neutral = sentiment_counts.get(1)
    cant_positivo = sentiment_counts.get(2)

    result = {
            f"Negativo: {cant_negativo}, Neutral: {cant_neutral}, Positivo: {cant_positivo}"   
        }
    
    return result




@app.get("/usersnotrecommend/{ano}")

async def UsersNotRecommend(ano:int):

    df = pd.read_csv('datasets/df_usersrecommend.csv')

    year_review = df[df['posted_year'] == ano]


    reviews_recommend = year_review[year_review['recommend'] == False] 

    sentiment_analysis_pos = reviews_recommend[reviews_recommend['sentiment_analysis'].isin([0])]

    review_games_pos = sentiment_analysis_pos['item_id'].value_counts()
    review_games_pos = review_games_pos.sort_values(ascending=False) #sigue siendo False porque son los que tienen mas reacciones negativas

    top_3 = review_games_pos.head(3)
    if top_3.empty:
        error = f"No se encontraron juegos recomendados para el año especificado."
        return error
    
    top_3_nombres = df[df['item_id'].isin(top_3.index)][['item_id', 'item_name']].value_counts()

    puesto1 = top_3_nombres.index[0][1]
    puesto2 = top_3_nombres.index[1][1]
    puesto3 = top_3_nombres.index[2][1]

    resultado = {
        f"Puesto 1:, {puesto1}, Puesto 2: {puesto2}, Puesto 3: {puesto3}"
    }

    return resultado




@app.get("/usersrecommend/{ano}")

async def UsersRecommend(ano:int): 
    df = pd.read_csv('datasets/df_usersrecommend.csv')

    year_review = df[df['posted_year'] == ano]


    reviews_recommend = year_review[year_review['recommend'] == True] 

    sentiment_analysis_pos = reviews_recommend[reviews_recommend['sentiment_analysis'].isin([1, 2])]

    review_games_pos = sentiment_analysis_pos['item_id'].value_counts()
    review_games_pos = review_games_pos.sort_values(ascending=False)

    top_3 = review_games_pos.head(3)
    if top_3.empty:
        error = f"No se encontraron juegos recomendados para el año especificado."
        return error
    
    top_3_nombres = df[df['item_id'].isin(top_3.index)][['item_id', 'item_name']].value_counts()

    puesto1 = top_3_nombres.index[0][1]
    puesto2 = top_3_nombres.index[1][1]
    puesto3 = top_3_nombres.index[2][1]

    resultado = {
        f"Puesto 1:, {puesto1}, Puesto 2: {puesto2}, Puesto 3: {puesto3}"
    }

    return resultado
