from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import static

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hojas_vida.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

@app.route('/')
def index():
   archivos = os.listdir("static")
   lista = []
   for a in archivos:
       if a.split(".")[1] in ["jpg", "png", "jpeg"]:
           lista.append(a)

   return render_template('index.html', msg = "file loaded successfully", rows = lista)

@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['POST'])
def uploader_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(app.root_path, 'static', secure_filename(f.filename)))

      archivos = os.listdir("static")
      lista = []
      for a in archivos:
          if a.split(".")[1] in ["jpg", "png", "jpeg"]:
              lista.append(a)

      return render_template('index.html', msg = "file loaded successfully", rows = lista)

@app.route('/drive')
def enviar():

    gauth = GoogleAuth()

    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    #file1 = drive.CreateFile({'tittle':'test.txt'})


    #file1.SetContentString('Hola Mundo primer intento')
    #file1.Upload()

    file5 = drive.CreateFile()
    # Read file and set it as a content of this instance.
    file5.SetContentFile('static\marce.jpg')
    file5.Upload() # Upload the file.
    print('title: %s, mimeType: %s' % (file5['title'], file5['mimeType']))
   
if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)