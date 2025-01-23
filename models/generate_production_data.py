import pandas as pd
import numpy as np
import joblib

# Chemins des fichiers
DATA_PATH = "/home/utilisateur/Documents/monitoring-app/data/creditcard.csv"
TEMP_MODEL_DATA_PATH = "/home/utilisateur/Documents/monitoring-app/models/temp_model_data.pkl"
PRODUCTION_DATA_PATH = "/home/utilisateur/Documents/monitoring-app/data/production_data.csv"

# Charger le modèle temporaire
def load_temp_model(temp_model_data_path):
    model, _, _ = joblib.load(temp_model_data_path)
    return model

# Charger les données de base
def load_base_data(data_path):
    df = pd.read_csv(data_path)
    df = df.drop(columns=["Time", "Class"])  # Supprimer les colonnes inutiles pour la simulation
    return df

# Générer des données fictives et ajouter les prédictions
def generate_production_data(base_data, model, num_samples=100000, threshold=0.2):
    # Prendre un échantillon des données existantes
    production_data = base_data.sample(n=num_samples, replace=True, random_state=42).copy()

    # Ajouter des variations pour simuler des nouvelles transactions
    noise = np.random.normal(0, 0.1, production_data.shape)
    production_data += noise

    # Simuler des montants (colonne 'Amount') plus variés
    if 'Amount' in production_data.columns:
        production_data['Amount'] = np.abs(production_data['Amount'] + np.random.normal(0, 10, len(production_data)))

    # Ajouter les prédictions du modèle en appliquant un threshold personnalisé
    probabilities = model.predict_proba(production_data)[:, 1]
    production_data['prediction'] = (probabilities >= threshold).astype(int)

    # Ajouter une colonne 'target' fictive pour les labels réels
    if 'target' not in production_data.columns:
        production_data['target'] = np.random.choice([0, 1], size=len(production_data), p=[0.98, 0.02])  # 2% de fraude

    return production_data

if __name__ == "__main__":
    print("Chargement du modèle et des données de base...")
    model = load_temp_model(TEMP_MODEL_DATA_PATH)
    base_data = load_base_data(DATA_PATH)

    print("Génération de données de production fictives...")
    production_data = generate_production_data(base_data, model, num_samples=100000, threshold=0.2)

    print(f"Sauvegarde des données de production fictives dans {PRODUCTION_DATA_PATH}...")
    production_data.to_csv(PRODUCTION_DATA_PATH, index=False)
    print("Données de production générées et sauvegardées avec succès.")

