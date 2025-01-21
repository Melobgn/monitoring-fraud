import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Chemins des fichiers
MODEL_PATH = "/home/utilisateur/Documents/monitoring-app/models/fraud_detection_model.pkl"
SCALER_PATH = "/home/utilisateur/Documents/monitoring-app/models/scaler.pkl"

# Charger le modèle et le scaler
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

def predict_fraud(data: pd.DataFrame, threshold=0.2):
    """
    Effectue une prédiction de fraude avec un threshold personnalisé.
    
    Args:
    - data (pd.DataFrame): Données d'entrée pour la prédiction.
    - threshold (float): Seuil pour classer une transaction comme frauduleuse.
    
    Returns:
    - prediction (int): 0 pour normal, 1 pour fraude.
    - probability (float): Probabilité associée à la classe 1 (fraude).
    """
    print("Données reçues pour prédiction :", data.head())

    # Normalisation de la colonne 'Amount'
    try:
        data['Amount'] = scaler.transform(data[['Amount']])
    except Exception as e:
        print("Erreur dans la normalisation :", e)
        raise

    # Faire la prédiction
    try:
        probability = model.predict_proba(data)[0][1]
        prediction = 1 if probability >= threshold else 0  # Application du threshold
        print("Prédiction :", prediction, "Probabilité :", probability)
    except Exception as e:
        print("Erreur lors de la prédiction :", e)
        raise

    return prediction, probability