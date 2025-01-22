from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from .schemas import Transaction
from .model import predict_fraud
import pandas as pd
import os
import traceback

# Initialisation de l'application FastAPI
app = FastAPI()

# Ajouter immédiatement l'instrumentation Prometheus
Instrumentator().instrument(app).expose(app)

LOG_CSV_PATH = "../data/api_requests_log.csv"

@app.post("/predict")
def predict(transaction: Transaction):
    try:
        # Vérifie que le répertoire existe, sinon le créer
        log_dir = os.path.dirname(LOG_CSV_PATH)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Convertir les données reçues en DataFrame
        input_data = pd.DataFrame([transaction.dict()])

        # Faire une prédiction
        prediction, probability = predict_fraud(input_data)

        # Enregistrer la requête et la prédiction
        log_data = input_data.copy()
        log_data['prediction'] = prediction
        log_data['probability'] = probability
        log_data.to_csv(LOG_CSV_PATH, mode='a', header=not os.path.exists(LOG_CSV_PATH), index=False)

        return {"prediction": int(prediction), "probability": float(probability)}

    except Exception as e:
        print("Erreur dans /predict :", traceback.format_exc())  # Afficher l'erreur complète
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction : {str(e)}")


# Endpoint de test basique
@app.get("/")
def root():
    return {"message": "API de prédiction pour la détection de fraudes"}

