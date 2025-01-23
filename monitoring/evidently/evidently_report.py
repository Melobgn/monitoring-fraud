import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, ClassificationPreset
from sklearn.metrics import classification_report

REFERENCE_DATA_PATH = "../../data/reference_data.csv"
PRODUCTION_DATA_PATH = "../../data/production_data.csv"

# Charger les données
reference_data = pd.read_csv(REFERENCE_DATA_PATH)
production_data = pd.read_csv(PRODUCTION_DATA_PATH)

reference_data['prediction'] = reference_data['prediction'].astype(int)
production_data['prediction'] = production_data['prediction'].astype(int)


print("Répartition des classes dans 'target' :")
print(reference_data['target'].value_counts(normalize=True))

print("\nRépartition des classes dans 'prediction' :")
print(reference_data['prediction'].value_counts(normalize=True))

# Évaluer les performances des prédictions pour le dataset de production
print("\nÉvaluation des prédictions pour le dataset de production :")
print(classification_report(production_data['target'], production_data['prediction'], zero_division=1))

# Créer le rapport Evidently AI
report = Report(metrics=[
    DataDriftPreset(),  # Analyse des dérives
    ClassificationPreset(),  # Analyse des performances
])

# Générer le rapport
report.run(reference_data=reference_data, current_data=production_data)

# Sauvegarder le rapport en HTML
report.save_html("./evidently_ai_report.html")
print("Rapport Evidently AI généré : evidently_ai_report.html")

