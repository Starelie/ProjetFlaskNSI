COLUMN_NUMBER = 3

function file_selection()
{
  let list = document.getElementById("files-list");
  let list_elements = list.children;
  for (let i = COLUMN_NUMBER + 1; i < list_elements.length; i += COLUMN_NUMBER) {
    list_elements[i].addEventListener("click", () => {
      if (!list_elements[i].classList.contains("selected")) {
        for (let j = COLUMN_NUMBER + 1; j < list_elements.length; j += COLUMN_NUMBER) {
          if (list_elements[j].classList.contains("selected")) {
            list_elements[j].firstChild.textContent = "select";
            list_elements[j].lastChild.textContent = "☐";
            list_elements[j].classList.remove("selected");
          }
        }
        list_elements[i].firstChild.textContent = "selected";
        list_elements[i].lastChild.textContent = "☑";
        list_elements[i].classList.add("selected");

        select_extension(list_elements[i + 1])
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

function select_extension(element)
{
  let selected_value = element.options[element.selectedIndex].value;
  document.getElementById("selected-extension").value = selected_value;
}

function extension_selection()
{
  let list = document.getElementById("files-list");
  let list_elements = list.children;
  for (let i = COLUMN_NUMBER + 2; i < list_elements.length; i += COLUMN_NUMBER) {
    list_elements[i].addEventListener("change", (element) => {
      if (list_elements[i - 1].classList.contains("selected"))
      {
        select_extension(element.currentTarget);
      }
    });
  }
}

function get_selected_file()
{
  let list = document.getElementById("files-list");
  let list_elements = list.children;
  for (let i = COLUMN_NUMBER + 1; i < list_elements.length; i += COLUMN_NUMBER) {
    if (list_elements[i].classList.contains("selected")) {
      return list_elements[i - 1].textContent
    }
  }
  return;
}

file_selection()
extension_selection()