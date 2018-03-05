
$(document).ready(function() {

    $('fieldset').hide();

    $('.btn').click(function() {
        $('.btn').removeClass('selected');
        $(this).addClass('selected');

        if ($('.btn.selected').length > 0) {
            $('fieldset').show(200);
        }
    });

    $('#tour_dates_table:has(td)').click(function(d) {
        var row = $(d.target).closest('tr');

        var show_date = row.find('td:eq(0)').text();
        var show_venue = row.find('td:eq(1)').text();

        $('#show_date_input').val(show_date);
        $('#show_venue_input').val(show_venue);

        $('#show_orig_date').val(show_date);
        $('#show_orig_venue').val(show_venue);
    });
});
