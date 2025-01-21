import joblib
import pandas as pd
import os

# Chemins des fichiers
TEMP_MODEL_DATA_PATH = "/home/utilisateur/Documents/monitoring-app/models/temp_model_data.pkl"
FINAL_MODEL_PATH = "/home/utilisateur/Documents/monitoring-app/models/fraud_detection_model.pkl"
REFERENCE_DATA_PATH = "/home/utilisateur/Documents/monitoring-app/data/reference_data.csv"

# Vérifier et créer les répertoires nécessaires
def ensure_directory_exists(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

# Charger le modèle temporaire et les données d'entraînement
def load_temp_model_data(temp_model_data_path):
    model, X_test, y_test = joblib.load(temp_model_data_path)
    return model, X_test  # On retourne X_test si nécessaire pour d'autres tâches

# Sauvegarder le modèle final
def save_model(model, model_path):
    try:
        ensure_directory_exists(model_path)
        joblib.dump(model, model_path)
        print(f"Modèle sauvegardé dans {model_path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du modèle : {e}")

# Sauvegarder le jeu de données de référence
def save_reference_data(X_train, reference_data_path):
    try:
        ensure_directory_exists(reference_data_path)
        if isinstance(X_train, pd.DataFrame):
            reference_data = X_train
        else:
            reference_data = pd.DataFrame(X_train, columns=[f"V{i}" for i in range(1, X_train.shape[1] + 1)])
        
        reference_data.to_csv(reference_data_path, index=False)
        print(f"Jeu de données de référence sauvegardé dans {reference_data_path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des données de référence : {e}")

if __name__ == "__main__":
    print("Chargement des données temporaires...")
    model, X_train = load_temp_model_data(TEMP_MODEL_DATA_PATH)

    print("Sauvegarde du modèle final...")
    save_model(model, FINAL_MODEL_PATH)

    print("Sauvegarde du jeu de données de référence...")
    save_reference_data(X_train, REFERENCE_DATA_PATH)

    print("Modèle et données de référence sauvegardés avec succès.")
