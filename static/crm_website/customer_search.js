function setDIVField(show, input_field)
{
    if ( show === null || input_field === null )
        return;
    if ( show )
    {
        input_field.show()
        input_field.children().prop('disabled', false);
    }
    else
    {
        input_field.hide();
        input_field.children().prop('disabled', true);
    }
}

$(document).ready( function() {
    setDIVField( this.checked, $('#id_paper_filter') );
    setDIVField( this.checked, $('#id_tax_sub_filter') );
    $('#id_papers').change( function() {
        setDIVField( this.checked, $('#id_paper_filter') );
    } );
    $('#id_tax_filter').change( function() {
        setDIVField( this.checked, $('#id_tax_sub_filter') );
    } );
});