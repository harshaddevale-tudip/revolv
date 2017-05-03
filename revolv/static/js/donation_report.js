$(document).ready(function () {
    table=$('#example').DataTable({
       <!--"dom": "Bfrtip",-->
       "dom": 'lfrtBip',
        "scrollX": true,
        buttons: [
           'csv', 'excel', 'print',
            {
                extend: 'pdfHtml5',
                orientation: 'landscape',
                pageSize: 'LEGAL'
            }
        ],
         "order": [[ 3, "desc" ]]
    })

    $.fn.dataTableExt.afnFiltering.push(
    function( oSettings, aData, iDataIndex ) {
        var iFini = document.getElementById('datepicker-1').value;
        var iFfin = document.getElementById('datepicker-2').value;
        var iStartDateCol = 3;
        var iEndDateCol = 3;

        var start_date=(iFini)? new Date(iFini):"";
        var end_date=(iFfin)? new Date(iFfin):"";
        start_date_list=new Date(new Date(aData[iStartDateCol]))
        end_date_list=new Date(new Date(aData[iStartDateCol]).setHours(0,0,0,0))

        if ( start_date == "" && end_date == "") {
            return true;
        }
        if ( start_date <= start_date_list && end_date == "") {
            return true;
        }
        else if ( end_date >= end_date_list && start_date == "") {
            return true;
        }
        else if (start_date <= start_date_list && end_date >= end_date_list ){
            return true;
        }
        else {
            return false;
        }

    }
);


} );

 $(function() {
            $( "#datepicker-1, #datepicker-2" ).datepicker({
            dateFormat: 'yy-mm-dd',
            onSelect: function(){table.draw();}
            }).keyup(function(e) {
            if(e.keyCode == 8 || e.keyCode == 46) {

                if (!$(this).value){
                    $.datepicker._clearDate(this);
                    table.draw();
                }


            }
        });
         });