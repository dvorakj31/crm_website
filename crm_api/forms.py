from django import forms
from .models import Customer, WarningEmail, CustomerFiles, CustomerHistory
from tempus_dominus.widgets import DatePicker

import datetime


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ()
        labels = {
            'name': 'Název subjektu',
            'address': 'Adresa',
            'email': 'Email',
            'ico': 'IČO',
            'dic': 'DIČ',
            'hea_insurance': 'Zdravotní pojišťovna',
            'var_symbol': 'Variabilní symbol soc. poj.',
            'soc_insurance': 'Sociální pojišťovna',
            'vat': 'Plátce DPH',
            'tax_office': 'Finanční úřad',
            'phone': 'Telefon',
            'tax_type': 'Typ daně',
            'tax_term': 'Termín daně'
        }


class CustomerFilesForm:
    class Meta:
        model = CustomerFiles


class WarningEmailForm(forms.ModelForm):
    class Meta:
        model = WarningEmail
        exclude = ()
        label = {
            'name': 'Název',
            'subject': 'Předmět emailu',
            'body': 'Tělo emailu',
        }


class ArchiveForm(forms.Form):

    date_field = forms.DateField(label="",
                                 widget=DatePicker(attrs={'append': 'fa fa-calendar', 'icon_toggle': True}),
                                 initial=datetime.date.today().isoformat())
