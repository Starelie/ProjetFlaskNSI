import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import pypandoc
import ffmpeg
from PIL import Image

# Déclarer les constantes
UPLOAD_FOLDER = "uploads/"
CONVERTED_FOLDER = "converted/"
TEMPLATE_FOLDER = "templates.folder/"
INPUT_EXTENSIONS_PILLOW = ("jpeg", "jpg", "png", "webp", "avif", "tiff", "gif")
OUTPUT_EXTENSIONS_PILLOW = ("jpeg", "jpg", "png", "webp", "avif", "tiff", "gif")
INPUT_EXTENSIONS_FFMPEG = ("ast", "avi", "flac", "gif", "h264", "hevc", "ico", "mov", "mp3", "mp4", "m4a", "wav")
OUTPUT_EXTENSIONS_FFMPEG = ("ast", "avi", "flac", "gif", "h264","hevc", "ico", "mov", "mp3", "mp4", "psp", "wav", "webm")
INPUT_EXTENSIONS_PANDOC = ("csv", "docx", "epub", "json", "html", "ipynb", "md", "odt", "pptx")
OUTPUT_EXTENSIONS_PANDOC = ("docx", "epub", "json", "html", "ipynb", "md", "odt", "pptx") 
ALLOWED_INPUT_EXTENSIONS = INPUT_EXTENSIONS_FFMPEG + INPUT_EXTENSIONS_PANDOC + INPUT_EXTENSIONS_PILLOW

# Initialiser flask
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["CONVERTED_FOLDER"] = CONVERTED_FOLDER
app.template_folder = TEMPLATE_FOLDER

# Créer des dossiers pour les fichiers uploadés et convertis si ces dossiers n'existent pas déjà
os.makedirs(os.path.relpath(UPLOAD_FOLDER), exist_ok=True)
os.makedirs(os.path.relpath(CONVERTED_FOLDER), exist_ok=True)


def split_filename(filename: str) -> list:
  '''
  filename: le nom d'un fichier en string
  Cette fonction sépare le nom du fichier de son extension, et si le nom est vide, le remplace par "no_name"
  retourne une liste contenant le nom du fichier et son extension (list)
  '''
  split = filename.rsplit(".", 1)
  if (split[0] == ""):
    split[0] = "no_name"
  return split


def allowed_file(filename: str) -> bool:
  '''
  filename: le nom d'un fichier en string
  Cette fonction vérifie que le fichier a une extension autorisée
  retourne True si le fichier a une extension autorisée, sinon False (boolean)
  '''
  return "." in filename and split_filename(filename)[1].lower() in ALLOWED_INPUT_EXTENSIONS


def lowercase_filename_extension(filename: str) -> str:
  '''
  filename: le nom d'un fichier en string
  Cette fonction met l'extension du fichier en minuscule pour éviter les problèmes de reconnaissance d'extension 
  retourne le nom du fichier avec l'extension en minuscule (string)
  '''
  splited_filename = split_filename(filename)
  clean_filename = splited_filename[0] + "." + splited_filename[1].lower()
  return clean_filename

def alphabetical_sort(filenames: list) -> list:
  '''
  filenames: une liste de noms de fichiers, en string
  Cette trie les noms de fichiers en ordre alphabétique
  retourne la liste de noms de fichiers, triée alphabétiquement (list)
  '''
  # transformer les lettres en nombres correspondants
  filenames_ascii_values = []
  for filename in filenames:
    filename_ascii_values = [0] * 200
    for char_index in range(len(filename)):
      filename_ascii_values[char_index] = ord(filename[char_index])
    filenames_ascii_values.append(filename_ascii_values)

  # trier la liste avec le tri par sélection
  for i in range(len(filenames_ascii_values) - 1):
    indice_du_mini = i
    for j in range(i + 1, len(filenames_ascii_values)) :
      indice_de_lettre = 0
      # ici, on trouve la première lettre qui n'est pas pareil pour ensuite la comparé
      while filenames_ascii_values[j][indice_de_lettre] == filenames_ascii_values[indice_du_mini][indice_de_lettre]:
        indice_de_lettre += 1
      if filenames_ascii_values[j][indice_de_lettre] < filenames_ascii_values[indice_du_mini][indice_de_lettre]:
        indice_du_mini = j
    for j in range(len(filenames_ascii_values[0])):
      filenames_ascii_values[i][j], filenames_ascii_values[indice_du_mini][j] = filenames_ascii_values[indice_du_mini][j], filenames_ascii_values[i][j]

  # transformer les nombres en lettres correspondantes
  filenames = []
  for filename_ascii_values in filenames_ascii_values:
    filename = ""
    for ascii in filename_ascii_values:
      if (ascii != 0):
        filename += chr(ascii)
    filenames.append(filename)
  return filenames

# fonction qui affiche la page d'accueil
@app.route("/")
def home():
  return render_template("home.html")


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
  '''
  Cette fonction affiche la page d'upload et gère les téléversements des fichiers
  retourne la page de téléversment.
  '''
  if request.method == "POST":
    file = request.files["file"]
    if file and allowed_file(file.filename):
      filename = secure_filename(lowercase_filename_extension(file.filename))
      file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
      return redirect(url_for("convert_file", name=filename))
  return render_template("upload.html")


@app.route("/download", methods=["GET", "POST"])
def download_file():
  '''
  Cette fonction affiche la page de téléchargement et gère le téléchargement des fichiers convertis
  retourne la page de téléchargement.
  '''
  files_names = alphabetical_sort(os.listdir(CONVERTED_FOLDER))
  if request.method == "GET":
    # S'il y a une requête GET, afficher le fichier demandé, sinon, afficher la sélection de fichiers
    try:
      file = request.args["downloaded_file"]
      return send_from_directory(app.config["CONVERTED_FOLDER"], file)
    except:
      return render_template("download.html", files=files_names)

@app.route("/convert", methods=["GET","POST"])
def convert_file():
  '''
  Cette fonction affiche la page de conversion et gère les conversions des fichiers uploadés
  retourne la page de conversion.
  '''
  # pour chaque fichier uploadé, on regarde quelles sont les extensions de sortie possibles en fonction de son extension, et on les ajoute à la liste des extension à afficher dans le sélecteur
  files = alphabetical_sort(os.listdir(UPLOAD_FOLDER))
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
    
  # si la méthode de la requete est POST, on récupère le fichier sélectionné et l'extension de sortie sélectionnée
  if request.method == "POST":
    selected = request.form.get("selected_file")
    extension = request.form.get("selected_extension")
    # vérifie s'il y a un fichier selectionné
    if selected is None:
      return render_template("convert.html", inputs=template_inputs)
    
    input_path = os.path.join(app.config["UPLOAD_FOLDER"], selected)

    # vérifie s'il y a une extension de sortie sélectionnée
    if not os.path.isfile(input_path):
      return render_template("convert.html", inputs=template_inputs)
    
    base_name, input_extension = split_filename(selected)
    output_filename = base_name + "." + extension
    output_path = os.path.join(app.config["CONVERTED_FOLDER"], output_filename)
    # en fonction de l'extension du fichier, on utilise la bibliothèque correspondante pour faire la conversion
    if (input_extension in INPUT_EXTENSIONS_PANDOC):
      pypandoc.convert_file(input_path, to=extension, outputfile=output_path)
    elif (extension in OUTPUT_EXTENSIONS_PILLOW and input_extension in INPUT_EXTENSIONS_PILLOW):
      Image.open(input_path).save(output_path)
    elif (extension in OUTPUT_EXTENSIONS_FFMPEG and input_extension in INPUT_EXTENSIONS_FFMPEG):
      ffmpeg.input(input_path).output(output_path).run()
    return redirect(url_for("download_file"))
  return render_template("convert.html", inputs=template_inputs)

# lance l'application flask en mode debug
if __name__ == "__main__":
  app.run(debug=True)
