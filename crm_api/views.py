from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic
from .models import Customer
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
# Create your views here.


class CustomerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Customer
    success_url = '/crm/'
    fields = '__all__'
    template_name = 'crm_api/table.html'
    login_url = '/crm/login/'


class CustomPasswordChangeForm(PasswordChangeForm):
    error_css_class = 'has-error'
    error_messages = {'password_incorrect': 'Nespravne heslo',
                      'password_mismatch': 'Hesla se neshoduji'}
    old_password = forms.CharField(required=True, label='Stare heslo',
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                   error_messages={'required': 'Vyplnte toto pole'})
    new_password1 = forms.CharField(required=True, label='Nove heslo',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                    error_messages={'required': 'Vyplnte toto pole'})
    new_password2 = forms.CharField(required=True, label='Potvrdte nove heslo',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                    error_messages={'required': 'Vyplnte toto pole'})


@login_required
def settings(request):
    return render(request, 'crm_api/settings.html')


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


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            # messages.success(request, 'Heslo uspesne zmeneno')
            return redirect('/crm')
        else:
            pass  # messages.error(request, 'Prosim, opravte chyby nize')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'crm_api/change_password.html', {
        'form': form
    })


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
