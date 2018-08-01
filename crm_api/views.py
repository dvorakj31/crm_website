from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.urls import reverse, reverse_lazy
from django.views import generic
from django import forms
from .models import Customer, WarningEmail, CustomerFiles
from django.conf import settings
import os
import mimetypes

PAGE_NUM = 7

# Create your views here.


@login_required
def edit_papers(request, cust_id):
    customer = get_object_or_404(Customer, pk=cust_id)
    customer.papers = not customer.papers
    customer.save()
    return HttpResponseRedirect('/crm')


@login_required
def download_file(request, file_id):
    cust_file = get_object_or_404(CustomerFiles, pk=file_id)
    file_name = str(cust_file.files)
    mime = mimetypes.guess_type(file_name)
    if mime[0] == None:
        mime = ('application/octet-stream', None)
    response = FileResponse(cust_file.files, content_type = 'file/%s' % mime[0].split('/')[1])
    response['Content-Disposition'] = "attachment;filename=%s" % file_name.split('/')[1]
    return response


@login_required
def select_customer(request):
    return render(request, 'crm_api/html/_search.html')


@login_required
def settings_view(request):
    return render(request, 'crm_api/html/settings.html')


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
    return render(request, 'crm_api/html/change_password.html', {
        'form': form
    })


@login_required
@permission_required('crm_api.add_warningemail')
def set_emails(request):
    if request.method == 'POST':
        val = request.POST.get('warningemail_id')
        return HttpResponseRedirect(reverse('crm_api:edit_email', kwargs={'pk': val}))
    return render(request, 'crm_api/html/set_emails.html', {'object_list': WarningEmail.objects.values()})
    
# Customer views starts here
class CustomerSearchList(LoginRequiredMixin, generic.ListView):
    model = Customer
    template_name = 'crm_api/html/customer_search_result.html'
    login_url = '/crm/login/'
    paginate_by = PAGE_NUM

    def get_queryset(self):
        query_set = Customer.objects.all()
        search_query = self.request.GET.get('q', None)
        search_filter = self.request.GET.get('filter_papers', None)
        query_set = Customer.objects.filter(name__contains='%s' % search_query)
        if search_filter != 'all' and search_filter in ['yes', 'no']:
            query_set = query_set.filter(papers__exact=search_filter == 'yes')
        return query_set


class CustomerList(LoginRequiredMixin, generic.ListView):
    model = Customer
    template_name = 'crm_api/html/index.html'
    login_url = '/crm/login/'
    paginate_by = PAGE_NUM


class CustomerCreateView(PermissionRequiredMixin, LoginRequiredMixin, generic.CreateView):
    permission_required = 'crm_api.add_customer'
    model = Customer
    success_url = '/crm/'
    fields = '__all__'
    template_name = 'crm_api/html/create_subject.html'
    login_url = '/crm/login/'


class CustomerUpdate(PermissionRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    permission_required = 'crm_api.change_customer'
    model = Customer
    template_name = 'crm_api/html/update_customer.html'
    fields = '__all__'
    success_url = '/crm/'
    login_url = '/crm/login/'


class CustomerDelete(PermissionRequiredMixin, LoginRequiredMixin, generic.DeleteView):
    permission_required = 'crm_api.delete_customer'
    model = Customer
    success_url = reverse_lazy('crm_api:index')
    fields = ['name']
    login_url = '/crm/login/'


# Customer file views starts here
class CustomerFilesCreateView(LoginRequiredMixin, generic.CreateView):
    model = CustomerFiles
    success_url = '/crm/'
    fields = ['files']
    template_name = 'crm_api/html/add_attachment.html'
    login_url = '/crm/login/'

    def form_valid(self, form):
        try:
            form.instance.customer = Customer.objects.get(pk=self.kwargs['cust_id'])
        except Customer.DoesNotExist:
            messages.error(self.request, 'Neplatny subjekt')
            return redirect('/crm/add_file/%s' % self.kwargs['cust_id'])
        return super(CustomerFilesCreateView, self).form_valid(form)


class CustomerFilesList(LoginRequiredMixin, generic.ListView):
    model = CustomerFiles
    template_name = 'crm_api/html/file_list.html'
    login_url = '/crm/login/'
    paginate_by = PAGE_NUM
    context_object_name = 'files'

    def get_queryset(self):
        try:
            file_obj = CustomerFiles.objects.filter(customer__id=self.kwargs['cust_id']).all()
        except CustomerFiles.DoesNotExist:
            file_obj = []
        return file_obj

    def get_context_data(self, **kwargs):
        context = super(CustomerFilesList, self).get_context_data(**kwargs)
        try:
            context['name'] = Customer.objects.get(pk=self.kwargs['cust_id']).name
        except:
            context['name'] = ''
        return context


class CustomerFilesDelete(PermissionRequiredMixin, LoginRequiredMixin, generic.DeleteView):
    permission_required = 'crm_api.delete_customerfiles'
    model = CustomerFiles
    success_url = reverse_lazy('crm_api:index')
    fields = ['files']
    login_url = '/crm/login/'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        print('trying to delete', os.path.join(settings.MEDIA_ROOT, str(obj.files)))
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, str(obj.files)))
        except:
            pass
        return super(CustomerFilesDelete, self).delete(request, args, kwargs)
    

# Settings views starts here
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


#Warning email views starts here
class WarningEmailCreateView(PermissionRequiredMixin, LoginRequiredMixin, generic.CreateView):
    permission_required = 'crm_api.add_warningemail'
    model = WarningEmail
    success_url = '/crm/set_emails'
    fields = '__all__'
    template_name = 'crm_api/html/create_email.html'
    login_url = '/crm/login/'


class WarningEmailUpdate(PermissionRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    permission_required = 'crm_api.change_warningemail'
    model = WarningEmail
    template_name = 'crm_api/html/update_email.html'
    fields = '__all__'
    success_url = '/crm/set_emails'
    login_url = '/crm/login/'


class WarningEmailDelete(PermissionRequiredMixin, LoginRequiredMixin, generic.DeleteView):
    permission_required = 'crm_api.delete_warningemail'
    model = WarningEmail
    success_url = reverse_lazy('crm_api:index')
    fields = ['name']
    login_url = '/crm/login/'
