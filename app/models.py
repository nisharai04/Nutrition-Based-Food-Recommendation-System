import pandas as pd
from sklearn.neighbors import NearestNeighbors
import requests
from .config import UNSPLASH_API_KEY  

def load_data(data_path="Anuvaad_INDB_2024.11 (1).csv"):
    """Load the food dataset."""
    return pd.read_csv(data_path)

def train_model(data):
    """Train a Nearest Neighbors model using numerical features."""
    features = data[[
        "fibre_g",
        "cholesterol_mg",
        "freesugar_g",
        "sodium_mg",
        "carb_g",
        "energy_kcal",
        "fat_g",
        "protein_g"
    ]]
    model = NearestNeighbors(n_neighbors=6)
    model.fit(features)
    return model

def get_recommendations(model, data, input_features):
    """Get recommendations based on input nutritional values."""
    distances, indices = model.kneighbors([input_features])
    recommendations = data.iloc[indices[0]]
    return recommendations

def get_image(query):
    """Fetch an image URL from Unsplash based on the food name."""
    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {UNSPLASH_API_KEY}"}
    params = {"query": query, "per_page": 1}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]['urls']['regular']  
    return "/static/images/default.jpg"  