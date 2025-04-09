FROM python:3.10-slim

# Installer les dépendances système
RUN apt update && apt install -y \
    tor \
    ffmpeg \
    curl \
    && apt clean

# Installer yt-dlp
RUN pip install yt-dlp

# Définir le dossier de travail
WORKDIR /app

# Copier les fichiers de l'app
COPY . /app

# Installer les dépendances Python
RUN pip install -r requirements.txt

# Lancer Tor et l'app Flask via Gunicorn
CMD gunicorn -b 0.0.0.0:$PORT app:app
