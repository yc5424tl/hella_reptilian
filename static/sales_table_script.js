
$(document).ready(function() {

    $('fieldset').hide();

    $('.btn').click(function() {
        $('.btn').removeClass('selected');
        $(this).addClass('selected');

        if ($('.btn.selected').length > 0) {
            $('fieldset').show(200);
        }
    });
});