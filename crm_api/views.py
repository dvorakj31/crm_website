from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from .models import Customer
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

# Create your views here.


class CustomerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Customer
    success_url = '/crm/'
    fields = '__all__'
    template_name = 'crm_api/table.html'
    login_url = '/crm/login/'


@login_required
def select_customer(request):
    if request.method == 'POST':
        val = request.POST.get('customer_id')
        return HttpResponseRedirect(reverse('crm_api:edit', kwargs={'pk': val}))
    return render(request, 'crm_api/select_customer.html', {'object_list': Customer.objects.values()})


@login_required
def delete_customer(request):
    if request.method == 'POST':
        val = request.POST.get('customer_id')
        return HttpResponseRedirect(reverse('crm_api:delete_customer', kwargs={'pk': val}))
    return render(request, 'crm_api/select_customer.html', {'object_list': Customer.objects.values()})


class IndexView(LoginRequiredMixin, generic.ListView):
    model = Customer
    template_name = 'crm_api/index.html'
    context_object_name = 'customer_list'
    login_url = '/crm/login'


class SelectCustomerListView(LoginRequiredMixin, generic.ListView):
    model = Customer
    template_name = 'crm_api/select_customer.html'
    context_object_name = 'object_list'
    login_url = '/crm/login/'


class CustomerUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Customer
    template_name = 'crm_api/table.html'
    fields = '__all__'
    success_url = '/crm/'
    login_url = '/crm/login/'


class CustomerDelete(LoginRequiredMixin, generic.DeleteView):
    model = Customer
    success_url = reverse_lazy('crm_api:index')
    fields = ['name']
    login_url = '/crm/login/'


class CustomerList(LoginRequiredMixin, generic.ListView):
    model = Customer
    template_name = 'crm_api/index.html'
    context_object_name = 'customer_list'
    login_url = '/crm/login/'
