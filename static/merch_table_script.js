

$(document).ready(function() {

    $('fieldset').hide();

    $('.btn').click(function() {
        $('.btn').removeClass('selected');
        $(this).addClass('selected');

        if ($('.btn.selected').length > 0) {
            $('fieldset').show(200);
        }
    });

    $('#merch_table:has(td)').click(function(d) {

        var td_row = $(d.target).closest('tr');

        var merch_name = td_row.find('td:eq(0)').text();
        var merch_cost = td_row.find('td:eq(1)').text();
        var merch_descr = td_row.find('td:eq(2)').text();

        $('#merch_name_input').val(merch_name);
        $('#merch_cost_input').val(merch_cost);
        $('#merch_descr_input').val(merch_descr);

        $('#merch_orig_name').val(merch_name);
        $('#merch_orig_cost').val(merch_cost);
        $('#merch_orig_descr').val(merch_descr);

    });
});


