let schema_url = dropdown.value;

//////////////////for using schematic API
getRequestedJson(schema_url).then((tangled_tree_data) => {
  let chart_dta = chart(tangled_tree_data);
  createCollapsibleTree(chart_dta, schema_url);
});

dropdown.addEventListener("change", function () {
  var schema_url = dropdown.value;
  console.log(schema_url);
  //////////////////for using schematic API
  getRequestedJson(schema_url).then((tangled_tree_data) => {
    var chart_dta = chart(tangled_tree_data);
    createCollapsibleTree(chart_dta, schema_url);
  });
});
