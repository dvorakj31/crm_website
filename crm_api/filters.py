import django_filters
from django_filters import widgets
from .models import Customer


BOOLEAN_CHOICES = (('', '--------'), ('false', 'Nepřinesl'), ('true', 'Přinesl'))


class CustomerFilter(django_filters.FilterSet):
    papers = django_filters.TypedChoiceFilter(widget=widgets.BooleanWidget, choices=BOOLEAN_CHOICES)
    road_tax_papers = django_filters.TypedChoiceFilter(widget=widgets.BooleanWidget, choices=BOOLEAN_CHOICES)
    name = django_filters.CharFilter(label='Název subjektu', lookup_expr='icontains')

    class Meta:
        model = Customer
        fields = []
