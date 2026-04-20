import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, send_file
from werkzeug.utils import secure_filename
import pypandoc
import ffmpeg
from PIL import Image

# Declare constants
UPLOAD_FOLDER = "uploads/"
CONVERTED_FOLDER = "converted/"
TEMPLATE_FOLDER = "templates.folder/"
INPUT_EXTENSIONS_PILLOW = ("jpeg", "jpg", "png", "webp", "avif", "tiff", "gif")
OUTPUT_EXTENSIONS_PILLOW = ("jpeg", "jpg", "png", "webp", "avif", "tiff", "gif")
INPUT_EXTENSIONS_FFMPEG = ("ast", "avi", "flac", "gif", "h264", "hevc", "ico", "mov", "mp3", "mp4", "m4a", "wav")
OUTPUT_EXTENSIONS_FFMPEG = ("ast", "avi", "flac", "gif", "h264","hevc", "ico", "ipod", "mov", "mp3", "mp4", "psp", "wav", "webm", "webp")
INPUT_EXTENSIONS_PANDOC = ("csv", "docx", "epub", "json", "html", "ipynb", "md", "odt", "pptx")
OUTPUT_EXTENSIONS_PANDOC = ("docx", "epub", "json", "html", "ipynb", "md", "odt", "pptx")
# OUTPUT_EXTENSIONS_PANDOC = ("docx", "epub", "json", "html", "ipynb", "md", "odt", "pdf", "pptx")
ALLOWED_INPUT_EXTENSIONS = INPUT_EXTENSIONS_FFMPEG + INPUT_EXTENSIONS_PANDOC + INPUT_EXTENSIONS_PILLOW

# Setup flask
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["CONVERTED_FOLDER"] = CONVERTED_FOLDER
app.template_folder = TEMPLATE_FOLDER

# Create necessary folders if they don't already exist
os.makedirs(os.path.relpath(UPLOAD_FOLDER), exist_ok=True)
os.makedirs(os.path.relpath(CONVERTED_FOLDER), exist_ok=True)

def split_filename(filename: str) -> list:
  split = filename.rsplit(".", 1)
  if (split[0] == ""):
    split[0] = "no_name"
  return split

def allowed_file(filename: str) -> bool:
  return "." in filename and split_filename(filename)[1].lower() in ALLOWED_INPUT_EXTENSIONS

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
      file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
      return redirect(url_for("convert_file", name=filename))
  return render_template("upload.html")

@app.route("/download", methods=["GET", "POST"])
def download_file():
  files_names = os.listdir(CONVERTED_FOLDER)
  if request.method == "GET":
    file = request.args["downloaded_file"]
    print(file)
    print(request.args["downloaded_file"])
    if (file == "select"):
      return render_template("download.html", files=files_names)
    else:
      return send_from_directory(app.config["CONVERTED_FOLDER"], file)

@app.route("/convert", methods=["GET","POST"])
def convert_file():
  files = os.listdir(UPLOAD_FOLDER)
  template_inputs = []
  for i in range(len(files)):
    extensions = []
    if split_filename(files[i])[1] in INPUT_EXTENSIONS_FFMPEG:
      extensions.extend(OUTPUT_EXTENSIONS_FFMPEG)
    if split_filename(files[i])[1] in INPUT_EXTENSIONS_PANDOC:
      extensions.extend(OUTPUT_EXTENSIONS_PANDOC)
    if split_filename(files[i])[1] in INPUT_EXTENSIONS_PILLOW:
      extensions.extend(OUTPUT_EXTENSIONS_PILLOW)
    template_inputs.append((files[i], extensions))
      
  if request.method == "POST":
    selected = request.form.get("selected_file")
    extension = request.form.get("selected_extension")

    if selected is None:
      return render_template("convert.html", inputs=template_inputs)
    
    input_path = os.path.join(app.config["UPLOAD_FOLDER"], selected)

    if not os.path.isfile(input_path):
      return render_template("convert.html", inputs=template_inputs)

    base_name, input_extension = split_filename(selected)
    output_filename = base_name + "." + extension
    output_path = os.path.join(app.config["CONVERTED_FOLDER"], output_filename)
    if (input_extension in INPUT_EXTENSIONS_PANDOC):
      pypandoc.convert_file(input_path, to=extension, outputfile=output_path)
    elif (extension in OUTPUT_EXTENSIONS_PILLOW and input_extension in INPUT_EXTENSIONS_PILLOW):
      Image.open(input_path).save(output_path)
    elif (extension in OUTPUT_EXTENSIONS_FFMPEG and input_extension in INPUT_EXTENSIONS_FFMPEG):
      ffmpeg.input(input_path).output(output_path).run()
    return redirect(url_for("download_file", downloaded_file="select"))
  return render_template("convert.html", inputs=template_inputs)

if __name__ == "__main__":
  app.run(debug=True)
