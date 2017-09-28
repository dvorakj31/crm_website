from django import forms


class CustomerForm(forms.Form):
    name = forms.CharField(label='Nazev spolecnosti', max_length=100)
    address = forms.CharField(label='adresa', max_length=100)
    ico = forms.CharField(label='ICO', max_length=20)
    dic = forms.CharField(label='DIC', max_length=20)
    email = forms.EmailField(label='email', max_length=254)
