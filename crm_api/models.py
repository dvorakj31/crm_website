from django.db import models

# Create your models here.


class Customer(models.Model):
    CHOICES_VAT = [
        ('mesicne', 'Mesicne'),
        ('ctvrtletne', 'Ctvrtletne')
    ]
    TAX_TYPES = [
        ('dpfo', 'DPFO'),
        ('dppo', 'DPPO')
    ]
    TAX_TERMS = [
        ('radny', 'Radny termin (1.4)'),
        ('odlozeny', 'Odlozeny termin (1.7)')
    ]
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=100)
    ico = models.CharField(max_length=20, blank=True, null=True)
    dic = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    tax_type = models.CharField(max_length=20, choices=TAX_TYPES, null=True)
    tax_term = models.CharField(max_length=25, choices=TAX_TERMS, null=True)
    vat = models.CharField(max_length=20, choices=CHOICES_VAT, null=True, blank=True)
    tax_office = models.CharField(max_length=254, blank=True, null=True)
    soc_insurance = models.CharField(max_length=254, blank=True, null=True)
    var_symbol = models.CharField(max_length=100, blank=True, null=True)
    hea_insurance = models.CharField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name
