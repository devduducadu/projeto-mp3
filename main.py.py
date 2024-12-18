# entrar no youtube procurar alguma musica ou video do seu gosto.

# copiar o link ou baixar o video para seu celular ou notebook.

# pesquisar no google um conversor de audio.

# no site deve ter as opçoes de colocar o video baixado ou a url do video

# colocando na opçao de video baixado ele vai abrir os arquivos do seu computador para voce escolher o video baixado. se caso escolha por url ele vai mostrar uma caixa para voce colocar a url do video

# após a escolha do usuario, devera ser feita a conversão. assim  possibilitando o download do mesmo.

# FIM

# quero criar um projeto de conversor de audios em python, no qual permite eu pegar o link ou baixar o video do youtube, entrar em meu proprio site e converter para mp3 entre outras formas de audi
#ok, agora eu preciso que voce especifique o que cada biblioeca e framework faz e o conceito e comandos de cada linha de codigo pois quero ter uma noçao e um aprendizado nesse projeto, quero estar por dentro de seus conceitos e detalhes de tudo que foi usado


# PASSO1 extrair audio do video.
import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from moviepy.editor import VideoFileClip

app = Flask(__name__)

# Diretórios para salvar uploads e conversões
UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'

# Criar diretórios se não existirem
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CONVERTED_FOLDER'] = CONVERTED_FOLDER

# Página principal para upload
@app.route('/')
def home():
    return render_template('index.html')

# Rota para upload de vídeo
@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return 'Nenhum arquivo foi enviado', 400

    file = request.files['file']
    if file.filename == '':
        return 'Nenhum arquivo foi selecionado', 400

    # Salvando o vídeo no diretório de uploads
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(video_path)

    # Converte o vídeo para MP3
    mp3_filename = file.filename.rsplit('.', 1)[0] + '.mp3'
    mp3_path = os.path.join(app.config['CONVERTED_FOLDER'], mp3_filename)

    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(mp3_path)
    except Exception as e:
        return f'Erro durante a conversão: {e}', 500

    return redirect(url_for('download_file', filename=mp3_filename))

# Rota para download do MP3 convertido
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['CONVERTED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
