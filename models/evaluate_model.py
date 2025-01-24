import joblib
from sklearn.metrics import classification_report, roc_auc_score

# Chemins des fichiers
TEMP_MODEL_DATA_PATH = "temp_model_data.pkl"
SCALER_PATH = "scaler.pkl"

# Charger le modèle, le scaler et les données de test
def load_model_and_data(temp_model_data_path, scaler_path):
    model, X_test, y_test = joblib.load(temp_model_data_path)
    scaler = joblib.load(scaler_path)
    return model, X_test, y_test, scaler

# Normaliser les données de test
def normalize_test_data(X_test, scaler):
    X_test['Amount'] = scaler.transform(X_test[['Amount']])
    return X_test

# Évaluer le modèle avec un threshold personnalisé
def evaluate_model_with_threshold(model, X_test, y_test, threshold=0.2):
    # Obtenir les probabilités pour la classe 1 (fraude)
    y_prob = model.predict_proba(X_test)[:, 1]

    # Appliquer le threshold pour générer les prédictions binaires
    y_pred = (y_prob >= threshold).astype(int)

    # Afficher le rapport de classification
    print(f"\nÉvaluation avec un threshold de {threshold}:")
    print(classification_report(y_test, y_pred))

# Calculer l'AUC-ROC
def calculate_auc_roc(model, X_test, y_test):
    y_prob = model.predict_proba(X_test)[:, 1]
    auc_score = roc_auc_score(y_test, y_prob)
    print(f"\nAUC-ROC : {auc_score:.2f}")

if __name__ == "__main__":
    print("Chargement du modèle, des données de test et du scaler...")
    model, X_test, y_test, scaler = load_model_and_data(TEMP_MODEL_DATA_PATH, SCALER_PATH)

    print("Normalisation des données de test...")
    X_test = normalize_test_data(X_test, scaler)

    print("Évaluation sur le jeu de test avec un threshold ajusté...")
    evaluate_model_with_threshold(model, X_test, y_test, threshold=0.2)

    print("Calcul de l'AUC-ROC...")
    calculate_auc_roc(model, X_test, y_test)
