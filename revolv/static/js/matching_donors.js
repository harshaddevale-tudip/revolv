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
  }]
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
    var id =$ (this).attr('data-id');
    $(this).closest('td').data()
    console.log(id);
    $.ajax({
      type: "GET",
      url: '/edit/',
      data: {id:id},
      success: function(response) {
        matchingDonor=JSON.parse(response.ProjectMatchingDonor);
         $('#id_User').val(matchingDonor[0].fields.matching_donor);
         $('#id_Project').val(matchingDonor[0].fields.project);
         $('#amount').val(matchingDonor[0].fields.amount);
         $('#matching_donor_id').val(matchingDonor[0].pk);
         $('#myModal').modal('toggle');
    }

    });
});

$('.matching-donor-add').click(function () {
    $('#id_User')[0].selectedIndex = 0;
    $('#id_Project')[0].selectedIndex = 0;
    $('#amount').val('');
    $("#matching-donor-save").prop('disabled', false);
})

$('#matching-donor-save').on('click', function () {
    var $frm = $('#add_matching_donor');
        amount=$('#amount').val();
        if (amount > 0) {
            console.log($('#id_User').val());
            $.ajax({
              type: "POST",
              url: '/add_matching_donor/',
              data : $frm.serialize(),
              success: function() {
                $('#myModal').modal('toggle');
                $("#matching-donor-save").prop('disabled', false);
                    setTimeout(function(){
                        location.reload();
                    }, 1000);
              }
        });
        }else{
            alert('Please enter correct amount');
        }

});

} );