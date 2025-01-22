import pandas as pd
import numpy as np
import joblib

# Chemins des fichiers
TEMP_MODEL_DATA_PATH = "/home/utilisateur/Documents/monitoring-app/models/temp_model_data.pkl"
PRODUCTION_DATA_PATH = "/home/utilisateur/Documents/monitoring-app/data/production_data.csv"

# Charger le modèle temporaire et les données de test
def load_temp_model_data(temp_model_data_path):
    model, X_test, y_test = joblib.load(temp_model_data_path)
    return model, X_test, y_test

# Générer des données fictives et ajouter les prédictions
def generate_production_data(X_test, model, num_samples=1000):
    # Prendre un échantillon des données existantes
    production_data = X_test.sample(n=num_samples, replace=True).copy()

    # Ajouter des variations pour simuler des nouvelles transactions
    noise = np.random.normal(0, 0.1, production_data.shape)
    production_data += noise

    # Simuler des montants (colonne 'Amount') plus variés
    if 'Amount' in production_data.columns:
        production_data['Amount'] = np.abs(production_data['Amount'] + np.random.normal(0, 10, len(production_data)))

    # Ajouter les prédictions du modèle
    production_data['prediction'] = model.predict(production_data)

    # Ajouter une colonne 'target' fictive pour les labels réels (si nécessaire)
    if 'target' not in production_data.columns:
        production_data['target'] = np.random.choice([0, 1], size=len(production_data), p=[0.98, 0.02])  # 2% de fraude

    return production_data

if __name__ == "__main__":
    print("Chargement des données temporaires...")
    model, X_test, y_test = load_temp_model_data(TEMP_MODEL_DATA_PATH)

    print("Génération de données de production fictives avec prédictions...")
    production_data = generate_production_data(X_test, model, num_samples=1000)

    print(f"Sauvegarde des données de production enrichies dans {PRODUCTION_DATA_PATH}...")
    production_data.to_csv(PRODUCTION_DATA_PATH, index=False)
    print("Données de production générées et sauvegardées avec succès.")