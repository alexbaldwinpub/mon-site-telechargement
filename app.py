from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    # Téléchargement de la vidéo avec yt-dlp
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Où la vidéo sera stockée
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({"message": "Video downloaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
