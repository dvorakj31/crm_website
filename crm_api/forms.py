from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ()
        labels = {
            'name': 'Nazev spolecnosti',
            'address': 'Adresa',
            'email': 'Email',
            'ico': 'ICO',
            'dic': 'DIC',
            'hea_insurance': 'Zdravotni pojistovna',
            'var_symbol': 'Variabilni symbol soc. poj.',
            'soc_insurance': 'Socialni pojistovna',
            'vat': 'Platce DPH',
            'tax_office': 'Financni urad',
            'phone': 'Telefon',
            'tax_type': 'Typ dane',
            'tax_term': 'Termin dane'
        }
