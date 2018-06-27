from django.db import models
# Create your models here.


class Customer(models.Model):
    CUSTOMER_LABELS = {
        'name': 'Nazev spolecnosti',
        'address': 'Adresa',
        'ico': 'ICO',
        'dic': 'DIC',
        'email': 'Email',
        'tax_type': 'Pravni subjekt',
        'tax_term': 'Termin platce',
        'vat': 'DPH',
        'tax_office': 'Financni urad',
        'soc_insurance': 'Socialni pojistovna',
        'var_symbol': 'Variabilni symbol socialniho pojisteni',
        'hea_insurance': 'Zdravotni pojistovna',
        'phone': 'Telefon',
        'papers': 'Prinesl Doklady',
        'road_tax': 'Silnicni dan',
        'property_tax': 'Dan z nemovitosti',
        'moss': 'MOSS',
        'employer': 'Zamestnavatel'
    }
    CHOICES_VAT = [
        ('mesicne', 'Mesicne'),
        ('ctvrtletne', 'Ctvrtletne')
    ]
    TAX_TYPES = [
        ('fo', 'Fyzicka osoba'),
        ('po', 'Pravnicka osoba')
    ]
    TAX_TERMS = [
        ('radny', 'Radny termin (1.4)'),
        ('odlozeny', 'Odlozeny termin (1.7)')
    ]
    name = models.CharField(max_length=100, unique=True, verbose_name=CUSTOMER_LABELS['name'])
    address = models.CharField(max_length=100, verbose_name=CUSTOMER_LABELS['address'])
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=CUSTOMER_LABELS['phone'])
    ico = models.CharField(max_length=20, blank=True, null=True, verbose_name=CUSTOMER_LABELS['ico'])
    dic = models.CharField(max_length=20, blank=True, null=True, verbose_name=CUSTOMER_LABELS['dic'])
    email = models.EmailField(max_length=254, blank=True, null=True, verbose_name=CUSTOMER_LABELS['email'])
    tax_type = models.CharField(max_length=20, choices=TAX_TYPES, default='fo',
                                verbose_name=CUSTOMER_LABELS['tax_type'])
    tax_term = models.CharField(max_length=25, choices=TAX_TERMS, null=True, verbose_name=CUSTOMER_LABELS['tax_term'])
    vat = models.CharField(max_length=20, choices=CHOICES_VAT, null=True, blank=True,
                           verbose_name=CUSTOMER_LABELS['vat'])
    tax_office = models.CharField(max_length=254, blank=True, null=True, verbose_name=CUSTOMER_LABELS['tax_office'])
    soc_insurance = models.CharField(max_length=254, blank=True, null=True,
                                     verbose_name=CUSTOMER_LABELS['soc_insurance'])
    var_symbol = models.CharField(max_length=100, blank=True, null=True, verbose_name=CUSTOMER_LABELS['var_symbol'])
    hea_insurance = models.CharField(max_length=254, blank=True, null=True,
                                     verbose_name=CUSTOMER_LABELS['hea_insurance'])
    papers = models.BooleanField(default=False, verbose_name=CUSTOMER_LABELS['papers'])
    road_tax = models.BooleanField(default=False, verbose_name=CUSTOMER_LABELS['road_tax'])
    property_tax = models.BooleanField(default=False, verbose_name=CUSTOMER_LABELS['property_tax'])
    moss = models.BooleanField(default=False, verbose_name=CUSTOMER_LABELS['moss'])
    is_employer = models.BooleanField(default=False, verbose_name=CUSTOMER_LABELS['employer'])

    def __str__(self):
        return self.name
