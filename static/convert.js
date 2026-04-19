let FFMPEG_FORMATS_FROM = ["avi", "h261", "h263", "h264", "hevc", "m4v", "mov", "mp3", "mp4", "wav", "webm"]
let FFMPEG_FORMATS_TO = ["avi", "h261", "h263", "h264", "hevc", "m4v", "mov", "mp3", "mp4", "wav", "webm"]
let PANDOC_FORMATS_FROM = ["csv", "docx", "docx", "epub", "json", "html", "ipynb", "md", "odt", "pptx"]
let PANDOC_FORMATS_TO = ["docx", "epub", "json", "html", "ipynb", "md", "odt", "pdf", "pptx"]

function file_selection()
{
  let list = document.getElementById("files-list");
  let list_elements = list.children;
  for (let i = 3; i < list_elements.length; i += 2) {
    list_elements[i].addEventListener("click", () => {
      if (!list_elements[i].classList.contains("selected")) {
        for (let j = 3; j < list_elements.length; j += 2) {
          if (list_elements[j].classList.contains("selected")) {
            list_elements[j].firstChild.textContent = "select";
            list_elements[j].lastChild.textContent = "☐";
            list_elements[j].classList.remove("selected");
          }
        }
        list_elements[i].firstChild.textContent = "selected";
        list_elements[i].lastChild.textContent = "☑";
        list_elements[i].classList.add("selected");
      }
      else {
        list_elements[i].firstChild.textContent = "select";
        list_elements[i].lastChild.textContent = "☐";
        list_elements[i].classList.remove("selected");
      }

      document.getElementById("selected-file").value = get_selected_file();
      document.getElementById("possible-convertions").value = get_possible_convertions();
    });
  }
}

function get_possible_convertions()
{
  var file = get_selected_file()
  file = file.split(".")
  let extension = file.at(file.length - 1)
  var possible_convertions = []
  if (extension in FFMPEG_FORMATS_FROM)
  {
    possible_convertions.concat(FFMPEG_FORMATS_TO)
  }
  if (extension in PANDOC_FORMATS_FROM)
  {
    possible_convertions.concat(PANDOC_FORMATS_TO)
  }
  console.log(possible_convertions)
  return possible_convertions
}

function get_selected_file()
{
  let list = document.getElementById("files-list");
  let list_elements = list.children;
  for (let i = 3; i < list_elements.length; i += 2) {
    if (list_elements[i].classList.contains("selected")) {
      return list_elements[i - 1].textContent
    }
  }
  return;
}

file_selection()