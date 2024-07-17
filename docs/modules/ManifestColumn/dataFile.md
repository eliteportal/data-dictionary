---
datatable: true
layout: page
parent: ManifestColumn
title: dataFile
---

{% assign mydata=site.data.dataFile %} 
{: .note-title } 
>dataFile
>
>Name of additional file(s) accompanying the data. The file(s) provide, for example, the name of any raw files generated by the instrument, generated reports from a vendor, an Rscript, or an instructions document. The files can be instrument raw files, converted peak lists such as mzML, MGF, or result files like mzIdentML. The files can be additional documentation submitted alongside the data needed for reuse and sharing purposes. Provide the file names of any additional files submitted alongside the data (ex., an ADAT file). Multiple file names can be separated by (;)Provide a value OR provide one of these values - Unknown Not collected, Not applicable, Not specified [[Source]](nan)
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
         targets: [4],
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