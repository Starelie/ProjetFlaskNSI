import os
import sqlite3
from flask import Flask, flash, request, redirect, send_file, url_for, render_template
from werkzeug.utils import secure_filename
import pypandoc
import ffmpeg

# Declare constants
UPLOAD_FOLDER = "uploads/"
DATABASE_FOLDER = "databases/"
TEMPLATE_FOLDER = "templates.folder/"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "html", "docx"}

# Setup flask
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.template_folder = TEMPLATE_FOLDER

# Create necessary folders if they don't already exist
os.makedirs(os.path.relpath(DATABASE_FOLDER), exist_ok=True)
os.makedirs(os.path.relpath(UPLOAD_FOLDER), exist_ok=True)

# Setup the database
connection = sqlite3.connect(f"{DATABASE_FOLDER}/uploads.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS uploads(filename, extension, time)")
cursor.close()
connection.close()

def split_filename(filename: str) -> list:
  split = filename.rsplit(".", 1)
  if (split[0] == ""):
    split[0] = "no_name"
  return split

def allowed_file(filename: str) -> bool:
  return "." in filename and split_filename(filename)[1].lower() in ALLOWED_EXTENSIONS

def add_file_database(filename: str) -> None:
  connection = sqlite3.connect(f"{DATABASE_FOLDER}/uploads.db")
  cursor = connection.cursor()
  table_entry = split_filename(filename)
  files = cursor.execute("SELECT filename, extension FROM uploads").fetchall()
  for (name, extension) in files:
    if name == table_entry[0] and extension == table_entry[1]:
      cursor.execute("DELETE FROM uploads WHERE filename = ? AND extension = ?", (name, extension))
  cursor.execute("""
                  INSERT INTO uploads (filename, extension, time)
                  VALUES (?, ?, CURRENT_TIMESTAMP)
                  """, table_entry)
  cursor.close()
  connection.commit()
  connection.close()

def lowercase_filename_extension(filename: str) -> str:
  splited_filename = split_filename(filename)
  clean_filename = splited_filename[0] + "." + splited_filename[1].lower()
  return clean_filename

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
  if request.method == "POST":
    file = request.files["file"]
    if file and allowed_file(file.filename):
      filename = secure_filename(lowercase_filename_extension(file.filename))
      add_file_database(filename)
      file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
      return redirect(url_for("convert_file", name=filename))
  return render_template("upload.html")

@app.route("/download")
def download_file():
  files_names = os.listdir(UPLOAD_FOLDER)
  return render_template("download.html", files=files_names)
'''
  print(os.path.join(app.config['UPLOAD_FOLDER'],))
  output = pypandoc.convert_file(os.path.join(app.config['UPLOAD_FOLDER'], files_names[0]), 'html')
  # output.file.save(os.path.join(app.config['UPLOAD_FOLDER'], "converted.html"))
'''
@app.route("/convert", methods=["GET","POST"])
def convert_file():
  files_names = os.listdir(UPLOAD_FOLDER)
  if request.method == "POST":
    selected = request.form.get("selected_file")

    if selected is None:
      return render_template("convert.html", files=files_names)
    
    input_path = os.path.join(app.config["UPLOAD_FOLDER"], selected)

    if not os.path.isfile(input_path):
      return render_template("convert.html", files=files_names)

    base_name, _ = os.path.splitext(selected)
    output_filename = base_name + ".docx"
    output = pypandoc.convert_file(input_path, 'docx', outputfile= os.path.join(app.config["UPLOAD_FOLDER"], output_filename))
    return redirect(url_for("download_file", name=files_names))
  return render_template("convert.html", files=files_names)

if __name__ == "__main__":
  app.run(debug=True)
