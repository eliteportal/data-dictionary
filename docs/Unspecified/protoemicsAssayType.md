---
datatable: true
layout: page
parent: Unspecified
title: protoemicsAssayType
---

{% assign mydata=site.data.protoemicsAssayType %} 
{: .note-title } 
>protoemicsAssayType
>
>Type of peptide quantification used (ex. Label Free) [[Source]](Sage Bionetworks,DSLWG,https://www.ebi.ac.uk/ols/ontologies/pride/termsiri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FPRIDE_0000514&viewMode=All&siblings=false)
<table id="myTable" class="display" style="width:100%">
    <thead>
    {% for column in mydata[0] %}
        <th>{{ column[0] }}</th>
    {% endfor %}
    </thead>
    <tbody>
    {% for row in mydata %}
        <tr>
        {% for cell in row %}
            <td>{{ cell[1] }}</td>
        {% endfor %}
        </tr>
    {% endfor %}
    </tbody>
</table>
<script type="text/javascript">
  $('#myTable').DataTable({
    responsive: {
        details: {
            display: $.fn.dataTable.Responsive.display.modal( {
                header: function ( row ) {
                    var data = row.data();
                    return 'Details for '+data[0];
                }
            } ),
            renderer: $.fn.dataTable.Responsive.renderer.tableAll({
                tableClass: "table"
            })
        }
    },
   "deferRender": true,
   "columnDefs": [
      { 
         targets: [3],
         render : function(data, type, row, meta){
            if(type === 'display' & data != 'Sage Bionetworks'){
               return $('<a>')
                  .attr('href', data)
                  .text(data)
                  .wrap('<div></div>')
                  .parent()
                  .html();} 
            if(type === 'display' & data == 'Sage Bionetworks'){
                return $('<a>')
                   .attr('href', 'https://sagebionetworks.org/')
                   .text(data)
                   .wrap('<div></div>')
                   .parent()
                   .html();
            
            } else {
               return data;
            }
         }
      } 
   ]
});
</script>