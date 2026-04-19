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
    });
  }
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