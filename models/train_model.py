import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report, roc_auc_score
import joblib

# Chemins des fichiers
DATA_PATH = "../data/creditcard.csv"
TEMP_MODEL_DATA_PATH = "temp_model_data.pkl"
SCALER_PATH = "scaler.pkl"
REFERENCE_DATA_PATH = "../data/reference_data.csv"

# Normaliser la colonne Amount
def normalize_amount(X):
    scaler = StandardScaler()
    X['Amount'] = scaler.fit_transform(X[['Amount']])
    return X, scaler

def load_and_prepare_data(data_path):
    df = pd.read_csv(data_path)
    df = df.drop(columns=['Time'])  # Supprimer la colonne 'Time'
    X = df.drop(columns=['Class'])
    y = df['Class']
    X, scaler = normalize_amount(X)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    return X_train, X_test, y_train, y_test, scaler

# Rééquilibrage des données
def balance_data(X_train, y_train):
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
    return X_train_resampled, y_train_resampled

# Entraîner le modèle
def train_model(X_train, y_train):
    model = RandomForestClassifier(random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    return model

def save_reference_data(X_test, y_test, model, reference_data_path):
    reference_data = X_test.copy()
    reference_data['target'] = y_test.values if hasattr(y_test, "values") else y_test

    # Ajouter les prédictions du modèle
    reference_data['prediction'] = model.predict(X_test)

    # Sauvegarder dans un fichier CSV
    reference_data.to_csv(reference_data_path, index=False)
    print(f"Jeu de données de référence sauvegardé dans {reference_data_path}")


if __name__ == "__main__":
    print("Chargement et préparation des données...")
    X_train, X_test, y_train, y_test, scaler = load_and_prepare_data(DATA_PATH)

    print("Rééquilibrage des données...")
    X_train_resampled, y_train_resampled = balance_data(X_train, y_train)

    print("Entraînement du modèle...")
    model = train_model(X_train_resampled, y_train_resampled)

    print("Sauvegarde du scaler...")
    joblib.dump(scaler, SCALER_PATH)
    print(f"Scaler sauvegardé dans {SCALER_PATH}")

    print("Évaluation sur le jeu de test...")
    y_pred = model.predict(X_test)
    print("Rapport de classification :")
    print(classification_report(y_test, y_pred))
    print("AUC-ROC :", roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]))

    print("Sauvegarde du modèle et des données de test...")
    joblib.dump((model, X_test, y_test), TEMP_MODEL_DATA_PATH)
    print(f"Modèle et données sauvegardés temporairement dans {TEMP_MODEL_DATA_PATH}")

    print("Génération du dataset de référence...")
    save_reference_data(X_test, y_test, model, REFERENCE_DATA_PATH)
