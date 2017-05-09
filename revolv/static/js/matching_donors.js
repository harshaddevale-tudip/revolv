$(document).ready(function() {
    table=$('#example').DataTable({
       "dom": 'lfrtBip',
        "scrollX": true,
        buttons: [],
        "columnDefs": [ {
        "targets": 3,
        "orderable": false
    } ],
     aoColumnDefs: [
  {
     bSortable: false,
     aTargets: [ 3,4 ]
  }
]
    })



$(".close-btn").click(function () {
    id=$(this).attr('data-id');
     var tr = $(this).closest('tr');
    if (confirm("Are you sure you want to delete this?")){
        $.ajax({
          type: "GET",
          url: '/delete/',
          data: {id:id},
          success: function() {
            tr.fadeOut(1000, function(){
                        $(this).remove();
                        table.row( tr ).remove().draw();
                    });

          }
        });
    }
});

$(".edit").click(function () {
    data=table.row( $(this).parents('tr') ).data();
    console.log(data[0]);
    id=$(this).attr('data-id');
    $(this).closest('td').data()
    $.ajax({
      type: "GET",
      url: '/edit/',
      data: {id:id},
      success: function(response) {
        matchingDonor=JSON.parse(response.ProjectMatchingDonor);
         $(id_User).val(matchingDonor[0].fields.matching_donor);
         $(id_Project).val(matchingDonor[0].fields.project);
         $(amount).val(matchingDonor[0].fields.amount);
         $(matching_donor_id).val(matchingDonor[0].pk);
         $('#myModal').modal('toggle');
    }

    });
});

$('.matching-donor-save').click(function () {
    var $frm = $('#add_matching_donor');
        $.ajax({
          type: $frm.attr('method'),
          url: '/add_matching_donor/',
          data : $frm.serialize(),
          success: function() {
            table.ajax.reload();
            $('#myModal').modal('toggle');
          }
    });

});

} );