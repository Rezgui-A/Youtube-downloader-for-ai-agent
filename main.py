from flask import Flask, request, jsonify, send_from_directory
import yt_dlp
import os
import uuid

app = Flask(__name__)
AUDIO_FOLDER = "audio"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@app.route('/download', methods=['POST'])
def download():
    url = request.json.get('url')
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_FOLDER, filename)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filepath,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return jsonify({"audio_url": f"/audio/{filename}"})

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory(AUDIO_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
