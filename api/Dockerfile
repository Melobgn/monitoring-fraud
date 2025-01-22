# Étape 1 : Utiliser une image Python légère
FROM python:3.9-slim

# Étape 2 : Définir le répertoire de travail
WORKDIR /app  # Nom du dossier dans le conteneur

# Étape 3 : Copier les dépendances nécessaires
COPY ../requirements.txt /api/requirements.txt

# Étape 4 : Installer les dépendances
RUN pip install --no-cache-dir -r /api/requirements.txt

# Étape 5 : Copier le contenu du dossier api dans le conteneur
COPY . /api

# Étape 6 : Exposer le port de l'API
EXPOSE 8000

# Étape 7 : Lancer l'application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

