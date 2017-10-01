from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from .forms import CustomerForm
from .models import Customer
# Create your views here.


def customer_form(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            f = form.save()
            return render(request, 'crm_api/thanks.html')

    else:
        form = CustomerForm()

    return render(request, 'crm_api/client.html', {'form': form})


def thanks(request):
    return render(request, 'crm_api/thanks.html')


def index(request):
    return render(request, 'crm_api/index.html')


def edit(request):
    return render(request, 'crm_api/edit.html', {'customer_list': Customer.objects.all().values_list()})


class EditListView(generic.ListView):
    model = Customer
    template_name = 'crm_api/edit.html'
    context_object_name = 'object_list'
