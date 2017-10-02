from django.shortcuts import render
from django.views import generic
from .models import Customer
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

# Create your views here.


class CustomerCreateView(generic.CreateView):
    model = Customer
    success_url = '/crm/'
    fields = '__all__'
    template_name = 'crm_api/client.html'


def thanks(request):
    return render(request, 'crm_api/thanks.html')


def index(request):
    return render(request, 'crm_api/index.html')


def select_customer(request):
    if request.method == 'POST':
        val = request.POST.get('customer_id')
        return HttpResponseRedirect(reverse('crm_api:edit', kwargs={'pk': val}))
    return render(request, 'crm_api/select_customer.html', {'object_list': Customer.objects.values()})


def delete_customer(request):
    if request.method == 'POST':
        val = request.POST.get('customer_id')
        return HttpResponseRedirect(reverse('crm_api:delete_customer', kwargs={'pk': val}))
    return render(request, 'crm_api/select_customer.html', {'object_list': Customer.objects.values()})


class SelectCustomerListView(generic.ListView):
    model = Customer
    template_name = 'crm_api/select_customer.html'
    context_object_name = 'object_list'


class CustomerUpdate(generic.UpdateView):
    model = Customer
    template_name = 'crm_api/customer_update.html'
    fields = '__all__'
    success_url = '/crm/'


class CustomerDelete(generic.DeleteView):
    model = Customer
    success_url = reverse_lazy('crm_api:index')
    fields = ['name']
