---
datatable: true
layout: page
parent: ''
title: HispanicorLatinoEthnicity
---

{% assign mydata=site.data.HispanicorLatinoEthnicity %} 
{: .note-title } 
>HispanicorLatinoEthnicity
>
>When ethnicity = Hispanic or Latino,Ethnicity of individual [[Source]](Sage Bionetworks,https://ncithesaurus.nci.nih.gov/ncitbrowser/pages/concept_details.jsfdictionary=NCI_Thesaurus&version=23.04d&code=C93563&ns=ncit&type=properties&key=1040179992&b=1&n=0&vse=null,https://www.synapse.org/#!Synapse:syn25878249)
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