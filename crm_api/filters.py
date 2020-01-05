import django_filters
from django_filters import widgets
from .models import Customer


EMPTY_CHOICE = ('', '--------')
PAPERS_CHOICES = (EMPTY_CHOICE, (True, 'Nepřinesl'), (True, 'Přinesl'))
TAX_CHOICES = (EMPTY_CHOICE, ('mesicne', 'Měsíčně'), ('ctvrtletne', 'Čtvrtletně'))
ROAD_TAX_CHOICES = (EMPTY_CHOICE, (True, 'Plátce'), (False, 'Neplátce'))


class CustomerFilter(django_filters.FilterSet):
    papers = django_filters.TypedChoiceFilter(label='Doklady DPH', widget=widgets.BooleanWidget, choices=PAPERS_CHOICES)
    road_tax = django_filters.TypedChoiceFilter(label='Silniční daň', widget=widgets.BooleanWidget,
                                                choices=ROAD_TAX_CHOICES)
    name = django_filters.CharFilter(label='Název subjektu', lookup_expr='icontains')
    ico = django_filters.CharFilter(label='IČO', lookup_expr='startswith')
    tax_term = django_filters.TypedChoiceFilter(choices=TAX_CHOICES)

    class Meta:
        model = Customer
        fields = []
