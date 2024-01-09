from flask import Flask, request, make_response, redirect, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from pytube import YouTube 
import random
#E Modulo pathlib sirve para manipular las rutas de sistemas de archivos
from pathlib import Path
import os 
app = Flask(__name__)

app.config['SECRET_KEY'] = 'any secret string'
class VideoForm(FlaskForm):
    video = StringField('Video URL', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html', error=error)

@app.route('/')
def index():
    #video_form = VideoForm()
    return render_template('index.html')

def on_progress(stream, chunk, bytes_remaining):
    """Callback function"""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size * 100
    print(f"Status: {round(pct_completed, 2)} %")

@app.route('/descargarVideo', methods=['POST'])
def descargar_video():
   if request.method == 'POST':
       try:
        urlVideo = request.form['url']
        videoYT = YouTube(urlVideo, on_progress_callback=on_progress)
        mp3 = videoYT.streams.filter(only_audio=True).first()
        path   = "Downloads" #Downloads, Documentos, Videos
        folder = "AudiosYT"
        #Directorio para almacenar las descargas
        url_Descargas = str(Path.home() / path)
           # download the file 
        out_file = mp3.download(output_path=os.path.join(url_Descargas, folder),filename=f"{videoYT.title}.mp3") 
        print(out_file)
        return render_template('Descarga.html', path=out_file)
       except Exception as e:
        return render_template('404.html', error=e)
   else:
        return render_template('index.html')



if __name__ == '__main__':
    app.run(port=5000, debug=True)