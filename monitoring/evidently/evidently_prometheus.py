import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from prometheus_client import Gauge, start_http_server
import time

# Chemins des fichiers
REFERENCE_DATA_PATH = "../../data/reference_data.csv"
PRODUCTION_DATA_PATH = "../../data/production_data.csv"

# Charger les données
reference_data = pd.read_csv(REFERENCE_DATA_PATH)
production_data = pd.read_csv(PRODUCTION_DATA_PATH)

# Créer un rapport de dérive Evidently
data_drift_report = Report(metrics=[
    DataDriftPreset()
])

# Gauges pour Prometheus
drift_score_gauge = Gauge("data_drift_score", "Score global de dérive des données")
drift_detected_gauge = Gauge("data_drift_detected", "Dérive détectée (1 si dérive, 0 sinon)")

# Fonction pour calculer et exposer les métriques
def calculate_and_export_metrics():
    data_drift_report.run(reference_data=reference_data, current_data=production_data)
    drift_results = data_drift_report.as_dict()

    # Extraire les résultats de la dérive
    data_drift_score = drift_results["metrics"][0]["result"]["dataset_drift"]
    drift_detected = int(data_drift_score > 0.5)  # Dérive détectée si le score dépasse 0.5

    # Mettre à jour les métriques Prometheus
    drift_score_gauge.set(data_drift_score)
    drift_detected_gauge.set(drift_detected)

if __name__ == "__main__":
    # Démarrer le serveur Prometheus
    start_http_server(8001)  # Serveur accessible sur le port 8001
    print("Serveur Prometheus pour le Data Drift démarré sur le port 8001")

    while True:
        calculate_and_export_metrics()
        time.sleep(30)  # Rafraîchir toutes les 30 secondes
