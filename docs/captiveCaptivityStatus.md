---
datatable: true
layout: page
parent: ''
title: captiveCaptivityStatus
---

{% assign mydata=site.data.captiveCaptivityStatus %} 
{: .note-title } 
>captiveCaptivityStatus
>
>When captivityStatus = captive,The status of the individual with regard to captivity. note: Wild, captive, and stranded values are applicable, especially for marine mammals. Depending on life stage terminology for individual species, other values are possible. Please let the data curation team know. [[Source]](-The%20duration%20of,-The%20status%20of,captivity%20duration,captivity%20status,https://www.animalaudiograms.org/audiogram_metadata_scheme#:~:text=of%20the%20animal.-,https://www.animalaudiograms.org/audiogram_metadata_scheme#:~:text=species%20are%20possible.-)
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