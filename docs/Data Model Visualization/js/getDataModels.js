let url =
  "https://raw.githubusercontent.com/Sage-Bionetworks/data_curator_config/main/dcc_config.csv";
var dropdown = document.getElementById("selection");

var schemaOptions = [];

fetch(url)
  .then((response) => response.text())
  .then((data) => {
    let rows = data.split("\n");
    for (let i = 0; i < rows.length; i++) {
      let cells = rows[i].split(",");
      for (let j = 0; j < cells.length - 1; j++) {
        if (j == 0 && i > 0) {
          var text = cells[j];
          var opt = document.createElement("option");
          opt.textContent = text;
          opt.value = cells[j + 2];
          dropdown.appendChild(opt);
        }
      }
    }
  })
  .catch((error) => console.log(error));

// console.log(dropdown);
