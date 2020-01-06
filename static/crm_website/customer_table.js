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

function set_insurance() {
    let val = $('#id_tax_type').val();
    if (val === 'po')
    {
        $('#id_soc_insurance').hide();
        $('label[for="id_soc_insurance"]').hide();
        $('#id_var_symbol').hide();
        $('label[for="id_var_symbol"]').hide();
        $('#id_hea_insurance').hide();
        $('label[for="id_hea_insurance"]').hide();
    }
    else if (val === 'fo')
    {
        $('#id_soc_insurance').show();
        $('label[for="id_soc_insurance"]').show();
        $('#id_var_symbol').show();
        $('label[for="id_var_symbol"]').show();
        $('#id_hea_insurance').show();
        $('label[for="id_hea_insurance"]').show();
    }
}

function set_vat() {
    let val = $('#id_vat').val();
    let papers = $('#id_papers');
    if(val === 'mesicne' || val === 'ctvrtletne')
    {
        $('label[for="id_papers"]').show();
        papers.show();
        papers.val("False")
    }
    else
    {
        $('label[for="id_papers"]').hide();
        papers.hide();
        papers.val("")
    }
}

$(document).ready(function(){
    set_vs();
    set_insurance();
    set_vat();
    $('#id_is_employer').click(set_vs);
    $('#id_tax_type').change(set_insurance);
    $('#id_vat').change(set_vat);
});
