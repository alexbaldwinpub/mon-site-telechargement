#!/bin/bash

# Variables
REPO_DIR="$HOME/mon-site-telechargement"  # <-- adapte le chemin si besoin
VIDEO_URL="https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Étape 1 : Aller dans le projet
cd "$REPO_DIR" || { echo "Dossier non trouvé : $REPO_DIR"; exit 1; }

# Étape 2 : Générer cookies.txt depuis Firefox ou Chrome (ici Firefox)
yt-dlp --cookies-from-browser firefox --cookies cookies.txt "$VIDEO_URL" --skip-download

# Étape 3 : Ajouter et push sur GitHub
git add cookies.txt
git commit -m "update: refresh cookies.txt"
git push

echo "✅ cookies.txt mis à jour et pushé sur GitHub avec succès."
