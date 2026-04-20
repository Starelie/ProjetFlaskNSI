COLUMN_NUMBER = 3

function file_selection()
{
  // trouver la liste de fichiers
  let list = document.getElementById("files-list");
  let list_elements = list.children;
  // si la colonne "Sélection" est cliquée
  for (let i = COLUMN_NUMBER + 1; i < list_elements.length; i += COLUMN_NUMBER) {
    list_elements[i].addEventListener("click", () => {
      // échanger entre "choisit" et "choisir" et enlever "choisit" des autres rangées
      if (!list_elements[i].classList.contains("selected")) {
        for (let j = COLUMN_NUMBER + 1; j < list_elements.length; j += COLUMN_NUMBER) {
          if (list_elements[j].classList.contains("selected")) {
            list_elements[j].firstChild.textContent = "choisir";
            list_elements[j].lastChild.textContent = "☐";
            list_elements[j].classList.remove("selected");
          }
        }
        list_elements[i].firstChild.textContent = "choisit";
        list_elements[i].lastChild.textContent = "☑";
        list_elements[i].classList.add("selected");

        // appeler select_extension pour que la bonne extension soit choisie
        select_extension(list_elements[i + 1])
      }
      else {
        list_elements[i].firstChild.textContent = "choisir";
        list_elements[i].lastChild.textContent = "☐";
        list_elements[i].classList.remove("selected");
      }

      document.getElementById("selected-file").value = get_selected_file();
    });
  }
}

function select_extension(element)
{
  // ajouter la valeur choisie dans le formulaire
  let selected_value = element.options[element.selectedIndex].value;
  document.getElementById("selected-extension").value = selected_value;
}

function extension_selection()
{
  // trouver la liste de fichiers
  let list = document.getElementById("files-list");
  let list_elements = list.children;
  // quand le sélecteur change, appeler select_extension
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
  // trouver quel fichier est choisit
  let list = document.getElementById("files-list");
  let list_elements = list.children;
  for (let i = COLUMN_NUMBER + 1; i < list_elements.length; i += COLUMN_NUMBER) {
    if (list_elements[i].classList.contains("selected")) {
      return list_elements[i - 1].textContent
    }
  }
  return;
}

// appeler les fonctions nécessaires
file_selection()
extension_selection()