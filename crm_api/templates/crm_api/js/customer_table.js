<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>

<script>
function set_vs() {
    if ($('#id_is_employer').is(':checked')) {
        $('#id_var_symbol_employees').show()
        $('label[for="id_var_symbol_employees"]').show();
    }
    else {
        $('#id_var_symbol_employees').hide()
        $('label[for="id_var_symbol_employees"]').hide();
    }

}
$(document).ready(function(){
    set_vs();
    $('#id_is_employer').click(set_vs);
    $('#id_tax_type').change(function() {
        var val = $('#id_tax_type').val()
        if (val === 'po')
        {
            $('#id_soc_insurance').hide()
            $('label[for="id_soc_insurance"]').hide();
            $('#id_var_symbol').hide()
            $('label[for="id_var_symbol"]').hide();
            $('#id_hea_insurance').hide()
            $('label[for="id_hea_insurance"]').hide();
        }
        else if (val === 'fo')
        {
            $('#id_soc_insurance').show();
            $('label[for="id_soc_insurance"]').show();
            $('#id_var_symbol').show()
            $('label[for="id_var_symbol"]').show();
            $('#id_hea_insurance').show()
            $('label[for="id_hea_insurance"]').show();
        }
    });

})
</script>
