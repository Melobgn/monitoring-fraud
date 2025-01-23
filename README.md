# Fraud Monitoring

## Description

Ce projet contient un système complet de détection de fraudes avec un système de monitoring intégré. L'application utilise FastAPI pour exposer une API de prédiction, et des outils comme Prometheus et Grafana pour le monitoring des métriques de l'API et des dérives de données, ainsi qu'un rapport complet Evidently AI pour monitorer le modèle de machine learning.


## Installation

1. Clonez le dépôt :
   ```
   git clone git@github.com:Melobgn/monitoring-fraud.git
   cd monitoring-fraud

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


1. **API**
   - **Dossier `api/`** : Contient le code source de l'API et son déploiement.
     - `app.py` : Point d'entrée de l'API. Contient les routes principales et les intégrations.
     - `schemas.py` : Définitions des schémas Pydantic pour valider les entrées.
     - `model.py` : Gère les prédictions du modèle de machine learning.
     - `Dockerfile` : Fichier Docker pour déployer l'API FastAPI.

2. **Données**
   - **Dossier `data/`** : Contient les jeux de données.
     - `creditcard.csv` : Jeu de données de base pour l'entraînement.
     - `reference_data.csv` : Données de référence utilisées pour comparer les dérives de données.
     - `production_data.csv` : Données simulées pour le suivi de la production.


3. **Modèles**
   - **Dossier `models/`** : Contient les modèles entraînés, les scripts et leurs métadonnées.
     - `__init__.py` : Fichier d'initialisation.
     - `data_exploration.py` : Script pour explorer les données.
     - `evaluate_model.py` : Évaluation des performances du modèle.
     - `fraud_detection_model.pkl` : Modèle final de détection de fraude.
     - `generate_production_data.py` : Génération de données fictives de production.
     - `save_model.py` : Sauvegarde du modèle et des données associées.
     - `scaler.pkl` : Scaler utilisé pour normaliser les données.
     - `temp_model_data.pkl` : Modèle et données de test sauvegardés temporairement.
     - `train_model.py` : Script d'entraînement du modèle.

4. **Monitoring**
   - **Dossier `monitoring/`** : Contient les outils et scripts pour le suivi et l'analyse.
     - **Evidently** : Scripts pour analyser les dérives avec Evidently AI.
       - `Dockerfile` : Fichier Docker pour déployer les scripts Evidently.
       - `evidently_ai_report.html` : Rapport HTML généré par Evidently.
       - `evidently_prometheus.py` : Intégration Evidently avec Prometheus pour surveiller le Data Drift.
       - `evidently_report.py` : Génère des rapports HTML pour analyser les dérives.
       - `requirements.txt` : Liste des dépendances Python pour Evidently.
     - **Grafana** : Contient les configurations nécessaires pour Grafana.
       - `dashboard.yml` : Indique quels dashboards Grafana doit charger.
       - `grafana_dashboard.json` : Modèle de tableau de bord Grafana.
     - **Prometheus** : Configuration de Prometheus pour surveiller les métriques.
       - `prometheus_config.yml` : Fichier de configuration Prometheus.

5. **Docker Compose**
   - **Fichier `docker-compose.yml`** : Gère le déploiement multi-conteneurs pour :
     - L'API FastAPI.
     - Prometheus pour la collecte des métriques.
     - Grafana pour la visualisation.
     - Evidently AI pour l'analyse des dérives du modèle.
     - Node Exporter pour le monitoring système.

