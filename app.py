from flask import Flask, request, jsonify, send_from_directory, render_template
import yt_dlp
import os
import re

app = Flask(__name__)

# Dossier pour les vidéos téléchargées
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return jsonify({
        "message": "Bienvenue sur le site de téléchargement ! Utilisez l'interface sur /interface ou POST sur /download."
    })

@app.route('/interface', methods=['GET', 'POST'])
def interface():
    if request.method == 'POST':
        url = request.form.get('url')

        # Vérifie si c’est une playlist
        if re.search(r'list=|playlist', url):
            return "❌ Les playlists ne sont pas autorisées."

        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'format': 'bestvideo+bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'nocheckcertificate': True,
            'cookies': 'cookies.txt',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0',
                'Accept-Language': 'fr-FR,fr;q=0.9',
            }
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            return f"✅ Vidéo téléchargée avec succès : <a href='/downloads/{os.path.basename(filename)}' download>Télécharger</a>"

        except Exception as e:
            return f"⚠️ Erreur lors du téléchargement : {str(e)}"

    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_api():
    data = request.get_json()

    if not data or 'url' not in data:
        return jsonify({"error": "URL manquante"}), 400

    url = data['url']

    # Vérifie si c’est une playlist
    if re.search(r'list=|playlist', url):
        return jsonify({"error": "Les playlists ne sont pas autorisées."}), 400

    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'cookies': 'cookies.txt',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0',
            'Accept-Language': 'fr-FR,fr;q=0.9',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return jsonify({
            "message": "Vidéo téléchargée avec succès",
            "filename": os.path.basename(filename)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
