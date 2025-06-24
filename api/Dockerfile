# Utiliser une image Python officielle légère
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le contenu du dossier local dans le conteneur
COPY . .

# Exposer le port 5001 (Flask écoute par défaut sur ce port)
EXPOSE 5001

# Commande pour lancer l’application Flask
CMD ["python", "app.py"]
