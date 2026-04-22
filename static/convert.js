COLUMN_NUMBER = 3

function file_selection()
{
  // trouver la liste de fichiers
  let second_column_list = document.getElementsByClassName("second-column");
  let third_column_list = document.getElementsByClassName("third-column");

  // si la colonne "Sélection" est cliquée
  for (let i = 0; i < second_column_list.length; i++) {
    if (!second_column_list[i].classList.contains("top-row"))
    {
      second_column_list[i].addEventListener("click", () => {
      // échanger entre "choisit" et "choisir" et enlever "choisit" des autres rangées
      if (!second_column_list[i].classList.contains("selected")) {
        for (let j = 0; j < second_column_list.length; j++) {
          if (second_column_list[j].classList.contains("selected")) {
            second_column_list[j].firstChild.textContent = "choisir";
            second_column_list[j].lastChild.textContent = "☐";
            second_column_list[j].classList.remove("selected");
          }
        }
        second_column_list[i].firstChild.textContent = "choisit";
        second_column_list[i].lastChild.textContent = "☑";
        second_column_list[i].classList.add("selected");

        // appeler select_extension pour que la bonne extension soit choisie
        select_extension(third_column_list[i])
      }
      else {
        second_column_list[i].firstChild.textContent = "choisir";
        second_column_list[i].lastChild.textContent = "☐";
        second_column_list[i].classList.remove("selected");
      }

      document.getElementById("selected-file").value = get_selected_file();
      });
    }
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
  let second_column_list = document.getElementsByClassName("second-column");
  let third_column_list = document.getElementsByClassName("third-column");

  // quand le sélecteur change, appeler select_extension
  for (let i = 0; i < third_column_list.length; i++) {
    third_column_list[i].addEventListener("change", (column_element) => {
      if (second_column_list[i].classList.contains("selected"))
      {
        select_extension(column_element.currentTarget);
      }
    });
  }
}

function get_selected_file()
{
  // trouver quel fichier est choisit
  let first_column_list = document.getElementsByClassName("first-column");
  let second_column_list = document.getElementsByClassName("second-column");
  for (let i = 0; i < second_column_list.length; i++) {
    if (second_column_list[i].classList.contains("selected")) {
      return first_column_list[i].textContent
    }
  }
  return;
}

// appeler les fonctions nécessaires
file_selection()
extension_selection()
