import os
import sqlite3
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

# Declare constants
UPLOAD_FOLDER = 'uploads/'
TEMPLATE_FOLDER = "templates.folder/"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Setup flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.template_folder = TEMPLATE_FOLDER

# Setup the database
os.makedirs(os.path.relpath(UPLOAD_FOLDER), exist_ok=True)
connection = sqlite3.connect(f"{UPLOAD_FOLDER}/uploads.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS uploads(filename, extension, time)")
cursor.close()
connection.close()

def allowed_file(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def add_file_database(filename: str) -> None:
  connection = sqlite3.connect("uploads/uploads.db")
  cursor = connection.cursor()
  split_filename = filename.rsplit('.', 1)
  table_entry = [split_filename[0], split_filename[1].lower()]
  cursor.execute("""
                  INSERT INTO uploads (filename, extension, time)
                  VALUES (?, ?, CURRENT_TIMESTAMP)
                  """, table_entry)
  cursor.close()
  connection.commit()
  connection.close()

@app.route('/')
def home():
    return render_template("base.html")

@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            add_file_database(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return render_template("upload.html")

@app.route("/download")
def download_file():
    return render_template("download.html")

@app.route("/convert")
def convert_file():
    return render_template("convert.html")

if __name__ == "__main__":
    app.run(debug=True)
