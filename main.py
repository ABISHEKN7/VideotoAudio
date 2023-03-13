from flask import Flask, render_template, request, send_from_directory
from flask import redirect, url_for
from moviepy import editor as me
import os
import time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    format = request.form['format']
    filetypes = [("Audio files", "*.mp3"), ("Audio files", "*.wav"), ("Audio files", "*.aiff"), ("Audio files", "*.flac"), ("Audio files", "*.wma"), ("Audio files", "*.ogg")]
    # Save the uploaded file to a temporary directory
    uploads_dir = 'uploads'
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    file_path = os.path.join(uploads_dir, file.filename)
    file.save(file_path)
    # Create a VideoFileClip object using the full file path
    video = me.VideoFileClip(file_path)
    audio = video.audio
    # Generate a unique filename based on the current timestamp
    timestamp = int(time.time())
    audio_file = f'converted_{timestamp}.mp3'
    downloads_dir = 'downloads'
    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)
    audio_path = os.path.join(downloads_dir, audio_file)
    audio.write_audiofile(audio_path)
    return render_template('index.html', fileName=audio_file)


@app.route('/download/<filename>')
def download(filename):
    download_dir = 'downloads'
    file_path = os.path.join(download_dir, filename)
    if os.path.exists(file_path):
        return send_from_directory(download_dir, filename, as_attachment=True)
    else:
        return "Error: file not found."


if __name__ == '__main__':
    app.run(debug=True)
