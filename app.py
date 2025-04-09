from flask import Flask, request, jsonify, send_from_directory
import os
import subprocess
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = './static'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL manquante'}), 400

    # ID unique pour ce téléchargement
    download_id = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_FOLDER, f"{download_id}.%(ext)s")

    # Commande yt-dlp via Tor
    cmd = [
        "torsocks", "yt-dlp",
        "-f", "mp4",
        "-o", output_path,
        url
    ]

    # Lancer le processus en arrière-plan
    subprocess.Popen(cmd)

    return jsonify({'download_id': download_id, 'status': 'started'})

@app.route('/status/<download_id>', methods=['GET'])
def check_status(download_id):
    for ext in ['mp4', 'mkv', 'webm']:
        path = os.path.join(DOWNLOAD_FOLDER, f"{download_id}.{ext}")
        if os.path.exists(path):
            return jsonify({'ready': True, 'filename': f"{download_id}.{ext}"})
    return jsonify({'ready': False})

@app.route('/static/<filename>')
def serve_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)
