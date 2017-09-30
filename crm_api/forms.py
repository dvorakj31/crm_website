from django import forms

CHOICES_TYPE = [('DPFO', (
    ('radny', 'Radny termin (1.4)'),
    ('odlozeny', 'Odlozeny termin (1.7)'),
)),
    ('DPPO', (
        ('radny', 'Radny termin (1.4)'),
        ('odlozeny', 'Odlozeny termin (1.7)')
    )),
]


CHOICES_VAT = [
    ('Platce DPH', (
        ('mesicne', 'Mesicne'),
        ('ctvrtletne', 'Ctvrtletne')
    ))
]


class CustomerForm(forms.Form):
    name = forms.CharField(label='Nazev spolecnosti', max_length=100)
    address = forms.CharField(label='Adresa', max_length=100)
    ico = forms.CharField(label='ICO', max_length=20, required=False)
    dic = forms.CharField(label='DIC', max_length=20, required=False)
    email = forms.EmailField(label='Email', max_length=254, required=False)
    tax = forms.ChoiceField(label='Typ platce', choices=CHOICES_TYPE, widget=forms.CheckboxSelectMultiple)
    vat = forms.ChoiceField(label='Platce DPH', choices=CHOICES_VAT, widget=forms.CheckboxSelectMultiple)
    tax_office = forms.CharField(label='Financni urad', max_length=254)
    soc_insurance = forms.CharField(label='Socialni pojistovna', max_length=254)
    var_symbol = forms.CharField(label='Variabilní symbol soc. poj.', max_length=100)
    hea_insurance = forms.CharField(label='Zdravotni pojistovna', max_length=254)
    phone = forms.CharField(label='Telefon', max_length=20, required=False)
