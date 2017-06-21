function clearInput() {
    $('input[name=check]').prop('checked', false);
    $('input[name=donation_amount_cents]').val('');
    $(".monthly-plan-msg").hide();
    $(".donate-popup .next-button").css("background-color", "#9a9a9a");
    $(".donate-popup .next-button").removeClass("stripe-button-el");
   $(".donate-popup .next-button").addClass("disable-donation-btn");
 }

function refreshpage() {
    location.reload();
 }

$(document).keydown(function(e) {
    // ESCAPE key pressed
    if (e.keyCode == 27) {
        $('#operationModal').modal('hide');
        location.reload();
    }
});

<!-- Commit Change -->
(function() {
    if(document.getElementById('commitchange-script')) return;
    var npo = 4642;
    var script = document.createElement('script');
    var first = document.getElementsByTagName('script')[0];
    script.setAttribute('data-npo-id', npo);
    script.id = 'commitchange-script';
    script.src = 'https://commitchange.com/js/donate-button.v2.js';
    first.parentNode.insertBefore(script, first);
})();

(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
ga('create', 'UA-26030992-4', 'auto');
ga('send', 'pageview');

