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

# Normaliser la colonne Amount
def normalize_amount(X):
    scaler = StandardScaler()
    X['Amount'] = scaler.fit_transform(X[['Amount']])
    return X, scaler  # Retourne également le scaler pour une utilisation future

def load_and_prepare_data(data_path):
    # Charger les données
    df = pd.read_csv(data_path)
    df = df.drop(columns=['Time'])  # Supprimer la colonne 'Time'

    # Séparer les features et la cible
    X = df.drop(columns=['Class'])
    y = df['Class']

    # Normaliser la colonne Amount
    X, scaler = normalize_amount(X)

    # Diviser les données en jeux d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    return X_train, X_test, y_train, y_test, scaler

# Rééquilibrage des données
def balance_data(X_train, y_train):
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
    return X_train_resampled, y_train_resampled

# Entraînement du modèle
def train_model(X_train, y_train):
    model = RandomForestClassifier(random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    return model

# Sauvegarder le scaler
def save_scaler(scaler, scaler_path):
    joblib.dump(scaler, scaler_path)
    print(f"Scaler sauvegardé dans {scaler_path}")

# Vérifications supplémentaires
def evaluate_train_test_distributions(y_train, y_test):
    print("\nRépartition des classes dans le jeu d'entraînement :")
    print(y_train.value_counts())
    print("\nRépartition des classes dans le jeu de test :")
    print(y_test.value_counts())

def calculate_auc_roc(model, X_test, y_test):
    y_prob = model.predict_proba(X_test)[:, 1]
    auc_score = roc_auc_score(y_test, y_prob)
    print(f"\nAUC-ROC : {auc_score:.2f}")

if __name__ == "__main__":
    print("Chargement et préparation des données...")
    X_train, X_test, y_train, y_test, scaler = load_and_prepare_data(DATA_PATH)

    print("Rééquilibrage des données...")
    X_train_resampled, y_train_resampled = balance_data(X_train, y_train)

    print("Entraînement du modèle...")
    model = train_model(X_train_resampled, y_train_resampled)

    print("Sauvegarde du scaler...")
    save_scaler(scaler, SCALER_PATH)

    print("Vérification des distributions des classes...")
    evaluate_train_test_distributions(y_train, y_test)

    print("Évaluation sur le jeu de test...")
    print("Rapport de classification :")
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    print("Calcul de l'AUC-ROC...")
    calculate_auc_roc(model, X_test, y_test)

    print("Sauvegarde temporaire du modèle et des données de test...")
    joblib.dump((model, X_test, y_test), TEMP_MODEL_DATA_PATH)
    print(f"Modèle et données sauvegardés temporairement dans {TEMP_MODEL_DATA_PATH}.")


