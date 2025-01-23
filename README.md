# Fraud Monitoring

## Description

Ce projet contient un système complet de détection de fraudes avec un système de monitoring intégré. L'application utilise FastAPI pour exposer une API de prédiction, et des outils comme Prometheus et Grafana pour le monitoring des métriques de l'API et des dérives de données, ainsi qu'un rapport complet Evidently AI pour monitorer le modèle de machine learning.


## Installation

1. Clonez le dépôt :
   ```
   git clone <URL_DU_DEPOT>
   cd monitoring-app

   ```


2. Installez les dépendances
    ```
    pip install -r requirements.txt
    ```

## Utilisation

### Lancer l'application avec Docker

1. Construisez et démarrez les services Docker : 
    ```
    docker compose up
    ```


### Endpoints de l'API

GET / : Endpoint de test basique.
POST /predict : Endpoint pour prédire une transaction frauduleuse.


### Tests

Pour exécuter les tests, utilisez pytest :
    ```
    pytest tests/
    ```


## Accès aux services de Monitoring

### Prometheus

Prometheus est configuré pour collecter les métriques de l'API et des dérives de données. Il est accessible sur http://localhost:9090.


### Grafana

Grafana est configuré pour visualiser les métriques collectées par Prometheus. Il est accessible sur http://localhost:3000 avec les identifiants par défaut :

Utilisateur : admin
Mot de passe : password123


### Evidently

Evidently est utilisé pour générer des rapports de dérive de données. Le serveur Prometheus pour Evidently est accessible sur http://localhost:8001.


## Structure du projet

- **api/** : Contient le code de l'API FastAPI
  - `app.py` : Point d'entrée principal de l'API
  - `schemas.py` : Définitions des schémas Pydantic
  - `model.py` : Gestion du modèle de machine learning
  - `__init__.py` : Fichier d'initialisation

- **data/** : Données utilisées pour l'entraînement et le monitoring
  - `creditcard.csv` : Jeu de données original (fraudes de carte de crédit)
  - `reference_data.csv` : Jeu de données de référence pour Evidently AI
  - `production_data.csv` : Données fictives de production générées

- **grafana/** : Configuration pour Grafana
  - **provisioning/** : Répertoire pour les dashboards et sources de données
    - **dashboards/** : Dashboards Grafana
      - `dashboard.yml` : Configuration de chargement des dashboards
      - `grafana_dashboard.json` : Modèle du tableau de bord Grafana
    - **datasources/** : Sources de données Grafana
      - `config.yml` : Configuration des sources Prometheus

- **models/** : Contient les modèles entraînés et leurs métadonnées
  - `temp_model_data.pkl` : Modèle et données de test sauvegardés temporairement
  - `scaler.pkl` : Scaler utilisé pour normaliser les données
  - `fraud_detection_model.pkl` : Modèle final de détection de fraude

- **monitoring/** : Code lié au monitoring
  - **evidently/** : Scripts Evidently AI
    - `evidently_report.py` : Génère un rapport Evidently
    - `__init__.py` : Fichier d'initialisation
  - **prometheus/** : Configuration Prometheus
    - `prometheus_config.yml` : Configuration de Prometheus pour les métriques

- **tests/** : Contient les tests unitaires
  - `test_api.py` : Tests pour l'API FastAPI
  - `__init__.py` : Fichier d'initialisation

- **venv/** : Environnement virtuel Python

- `.gitignore` : Fichiers à ignorer par Git

- `dashboard.png` : Capture d'écran du tableau de bord Grafana

- `docker-compose.yml` : Configuration Docker pour tout le projet

- `README.md` : Documentation du projet

- `requirements.txt` : Dépendances Python du projet




## Explications des composants en détails

1. API
Le dossier api/ contient le code source de l'API, développée avec FastAPI.

app.py : Point d'entrée de l'API. Contient les routes principales et les intégrations.
schemas.py : Définitions des schémas Pydantic pour valider les entrées.
model.py : Gère les prédictions du modèle de machine learning.

2. Données
Le dossier data/ contient :

creditcard.csv : Jeu de données de base pour l'entraînement.
reference_data.csv : Données de référence utilisées pour comparer les dérives de données.
production_data.csv : Données simulées pour le suivi de la production.

3. Modèles
Le dossier models/ contient :

temp_model_data.pkl : Sauvegarde temporaire du modèle et des données de test.
scaler.pkl : Scaler utilisé pour normaliser les données.
fraud_detection_model.pkl : Modèle entraîné final.

4. Monitoring
Le dossier monitoring/ est utilisé pour le suivi :

evidently/ : Scripts pour analyser les dérives avec Evidently AI.
evidently_report.py : Génère des rapports en HTML.
grafana/ contient les configurations nécessaires pour Grafana :
dashboard.yml : Indique quels dashboards Grafana doit charger.
grafana_dashboard.json : Modèle de tableau de bord Grafana.
prometheus/ : Configuration de Prometheus.

6. Docker Compose
Le fichier docker-compose.yml gère le déploiement multi-conteneurs pour :

L'API FastAPI
Prometheus pour les métriques
Grafana pour la visualisation
Evidently AI pour le modèle de machine learning
Node Exporter pour le monitoring système

