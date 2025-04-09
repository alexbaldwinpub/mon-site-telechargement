import os
import subprocess
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            try:
                process = subprocess.run(
                    ["yt-dlp", "--proxy", "socks5h://127.0.0.1:9050", url],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                result = process.stdout or process.stderr
            except Exception as e:
                result = str(e)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
