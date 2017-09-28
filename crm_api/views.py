from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import CustomerForm
# Create your views here.


def customer_form(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('thanks/')

    else:
        form = CustomerForm()

    return render(request, 'crm_api/customer.html', {'form': form})


def thanks(request):
    return render(request, 'crm_api/thanks.html')
