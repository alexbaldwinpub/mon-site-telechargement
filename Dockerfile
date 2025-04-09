FROM python:3.10-slim

# Installer les dépendances système
RUN apt update && apt install -y \
    tor \
    ffmpeg \
    curl \
    && apt clean

# Installer yt-dlp et dépendances Python
RUN pip install yt-dlp

# Créer le dossier de l'application
WORKDIR /app

# Copier les fichiers dans le conteneur
COPY . /app

# Installer les dépendances Python
RUN pip install -r requirements.txt

# Lancer Tor + l'app Flask via Gunicorn
CMD tor & gunicorn -b 0.0.0.0:$PORT app:app
 
