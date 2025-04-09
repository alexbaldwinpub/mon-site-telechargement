from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import subprocess
import uuid

app = Flask(__name__, template_folder='templates')
DOWNLOAD_FOLDER = './static'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Route d'accueil pour afficher index.html
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

# Lancement du téléchargement
@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL manquante'}), 400

    download_id = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_FOLDER, f"{download_id}.%(ext)s")

    # Commande yt-dlp avec torsocks
    cmd = [
        "torsocks", "yt-dlp",
        "-f", "mp4",
        "-o", output_path,
        url
    ]

    subprocess.Popen(cmd)

    return jsonify({'download_id': download_id, 'status': 'started'})

# Vérification du statut
@app.route('/status/<download_id>', methods=['GET'])
def check_status(download_id):
    for ext in ['mp4', 'mkv', 'webm']:
        path = os.path.join(DOWNLOAD_FOLDER, f"{download_id}.{ext}")
        if os.path.exists(path):
            return jsonify({'ready': True, 'filename': f"{download_id}.{ext}"})
    return jsonify({'ready': False})

# Accès au fichier une fois téléchargé
@app.route('/static/<filename>')
def serve_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)
