from flask import Flask, request, jsonify, render_template, send_from_directory
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    if request.is_json:
        data = request.get_json()
        url = data.get('url')
    else:
        url = request.form.get('url')

    if not url:
        return jsonify({'error': 'Aucune URL fournie'}), 400

    try:
        unique_id = str(uuid.uuid4())
        filename = unique_id + ".mp4"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)

        ydl_opts = {
            'outtmpl': filepath,
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'quiet': True,
            'cookiefile': os.path.expanduser('cookies.txt'),  # <= cookies ajoutés ici
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return jsonify({'filename': filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/downloads/<path:filename>')
def serve_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
