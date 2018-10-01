from jchart import Chart
from jchart.config import DataSet
from .models import Customer

class TaxSubPieChart(Chart):
    chart_type = 'pie'
    responsive = False

    def get_datasets(self, **kwargs):
        tax_pay = Customer.objects.filter(vat__in=['ctvrtletne', 'mesicne'])
        submitted = tax_pay.filter(submitted_tax=True)
        return [{
            'label': 'Podaná přiznání',
            'data': [len(submitted), len(tax_pay) - len(submitted)],
            'backgroundColor': ["#FF6384", "#36A2EB"],
            'hoverBackgroundColor': ["#FF6384", "#36A2EB"],
        }]

    def get_labels(self, **kwargs):
        return ['Podaná přiznání', 'Nepodaná přiznání']


class PapersPieChart(Chart):
    chart_type = 'pie'
    responsive = False

    def get_datasets(self, **kwargs):
        all_customers_cnt = len(Customer.objects.all())
        papers_cnt = len(Customer.objects.filter(papers=True))
        return [{
            'label': 'Donesené doklady',
            'data': [papers_cnt, all_customers_cnt - papers_cnt],
            'backgroundColor': ["#FF6384", "#36A2EB"],
            'hoverBackgroundColor': ["#FF6384", "#36A2EB"],
        }]

    def get_labels(self, **kwargs):
        return ['Donesené doklady', 'Nedonesené doklady']
