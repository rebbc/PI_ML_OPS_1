from fastapi import FastAPI
import pandas as pd

df_steams = pd.read_csv('data_outputs.csv') 
df_review = pd.read_csv('data_user.csv')

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