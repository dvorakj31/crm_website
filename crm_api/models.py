from django.db import models
from django.core.validators import RegexValidator
import os
# Create your models here.


class Customer(models.Model):    
    CUSTOMER_LABELS = {
        'name': 'Název subjektu',
        'address': 'Adresa',
        'ico': 'IČO',
        'dic': 'DIČ',
        'email': 'Email',
        'tax_type': 'Právní subjekt',
        'tax_term': 'Termín podání přiznání - daň z příjmu',
        'vat': 'DPH',
        'tax_office': 'Finanční úřad',
        'soc_insurance': 'Sociální pojišťovna',
        'var_symbol': 'Variabilní symbol sociálního pojištění',
        'hea_insurance': 'Zdravotní pojišťovna',
        'phone': 'Telefon',
        'papers': 'Přinesl doklady k DPH',
        'wage': 'Mzdové podklady',
        'road_tax': 'Plátce silniční daně',
        'advance_tax': 'Zpracovaná zálohová daň',
        'withholding_tax': 'Zpracovaná srážková daň',
        'property_tax': 'Daň z nemovitosti',
        'moss': 'MOSS',
        'employer': 'Zaměstnavatel',
        'var_symbol_employees': 'Variabilní symbol zaměstnanci',
        'sub_tax': 'Podané přiznání DPH',
        'sub_road_tax': 'Podané přiznání silniční daně',
        'sub_wage': 'Zpracované mzdy',
    }
    CHOICES_VAT = [
        ('neplatce', 'Neplátce'),
        ('mesicne', 'Mesíčně'),
        ('ctvrtletne', 'Čtvrtletně')
    ]
    TAX_TYPES = [
        ('fo', 'Fyzická osoba'),
        ('po', 'Právnická osoba')
    ]
    TAX_TERMS = [
        ('radny', 'Řádný termín (1.4.)'),
        ('odlozeny', 'Odložený termín (1.7.)')
    ]
    PAPERS_TYPES = [
        (True, 'Přinesl'),
        (False, 'Nepřinesl'),
    ]

    name = models.CharField(max_length=100, verbose_name=CUSTOMER_LABELS['name'], 
                            validators=[RegexValidator(r'^\w(\w|\s|\.|,)*$',
                                                       'Povoleny jsou pouze znaky a-ž A-Ž 0-9 . , a mezera')])
    address = models.CharField(max_length=100, verbose_name=CUSTOMER_LABELS['address'])
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=CUSTOMER_LABELS['phone'])
    ico = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name=CUSTOMER_LABELS['ico'])
    dic = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name=CUSTOMER_LABELS['dic'])
    email = models.EmailField(max_length=254, blank=True, null=True, verbose_name=CUSTOMER_LABELS['email'])
    tax_type = models.CharField(max_length=20, choices=TAX_TYPES, default='fo',
                                verbose_name=CUSTOMER_LABELS['tax_type'])
    tax_term = models.CharField(max_length=25, choices=TAX_TERMS, null=True, default='radny',
                                verbose_name=CUSTOMER_LABELS['tax_term'])
    vat = models.CharField(max_length=20, choices=CHOICES_VAT, default='neplatce',
                           verbose_name=CUSTOMER_LABELS['vat'])
    tax_office = models.CharField(max_length=254, blank=True, null=True, verbose_name=CUSTOMER_LABELS['tax_office'])
    soc_insurance = models.CharField(max_length=254, blank=True, null=True,
                                     verbose_name=CUSTOMER_LABELS['soc_insurance'])
    var_symbol = models.CharField(max_length=100, blank=True, null=True, verbose_name=CUSTOMER_LABELS['var_symbol'])
    hea_insurance = models.CharField(max_length=254, blank=True, null=True,
                                     verbose_name=CUSTOMER_LABELS['hea_insurance'])
    papers = models.BooleanField(null=True, blank=True, verbose_name=CUSTOMER_LABELS['papers'], choices=PAPERS_TYPES)
    wage = models.BooleanField(default=False, verbose_name=CUSTOMER_LABELS['wage'])
    advance_tax = models.BooleanField(default=False, verbose_name=CUSTOMER_LABELS['advance_tax'])
    withholding_tax = models.BooleanField(default=False, verbose_name=CUSTOMER_LABELS['withholding_tax'])
    property_tax = models.BooleanField(default=False, verbose_name=CUSTOMER_LABELS['property_tax'])
    road_tax = models.BooleanField(default=False, verbose_name=CUSTOMER_LABELS['road_tax'])
    moss = models.BooleanField(default=False, verbose_name=CUSTOMER_LABELS['moss'])
    is_employer = models.BooleanField(default=False, verbose_name=CUSTOMER_LABELS['employer'])
    var_symbol_employees = models.CharField(max_length=100, blank=True, null=True,
                                            verbose_name=CUSTOMER_LABELS['var_symbol_employees'])
    submitted_tax = models.BooleanField(default=False, verbose_name=CUSTOMER_LABELS['sub_tax'])
    submitted_road_tax = models.BooleanField(default=False, verbose_name=CUSTOMER_LABELS['sub_road_tax'])
    submitted_wage_tax = models.BooleanField(default=False, verbose_name=CUSTOMER_LABELS['sub_wage'])

    def __str__(self):
        return self.name


class CustomerFiles(models.Model):
    files = models.FileField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='files')
    file_path = models.CharField(max_length=255)

    def filename(self):
        return os.path.basename(self.files.name)

    def is_dir(self):
        return os.path.isdir(self.files.name)

    def __str__(self):
        return self.files.name


class WarningEmail(models.Model):
    MAIL_TYPES = [
        ('lvl1', 'První varování'),
        ('lvl2', 'Druhé varování'),
        ('lvl3', 'Třetí varování'),
    ]

    DATE_NUMBERS = [
        (x, y) for x, y in zip([x for x in range(1, 29)], [str(y) for y in range(1, 29)])
    ]

    name = models.CharField(max_length=20, verbose_name='Název')
    subject = models.CharField(max_length=20, verbose_name='Předmět')
    body = models.TextField(max_length=500, verbose_name='Tělo')
    mail_type = models.CharField(max_length=20, choices=MAIL_TYPES, default='lvl1', verbose_name='Druh varování')
    send_date = models.IntegerField(choices=DATE_NUMBERS, default=1, verbose_name='Číslo dne odeslání')

    def __str__(self):
        return self.name
