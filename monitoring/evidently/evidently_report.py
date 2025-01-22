import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, ClassificationPreset

REFERENCE_DATA_PATH = "../../data/reference_data.csv"
PRODUCTION_DATA_PATH = "../../data/production_data.csv"

# Charger les données
reference_data = pd.read_csv(REFERENCE_DATA_PATH)
production_data = pd.read_csv(PRODUCTION_DATA_PATH)

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

