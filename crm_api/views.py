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
from .forms import CustomerFilesForm
from django.conf import settings
import os, sys
import mimetypes
import re

PAGE_NUM = 7

# Auxiliary functions


# Create your views here.

class CFile:
    
    def __init__(self, path):
        self.path = path
    
    def isdir(self):
        return os.path.isdir(self.path)

    def filename(self):
        return os.path.basename(self.path)

    def __lt__(self, other):
        return self.filename < other.filename
        

@login_required
def edit_papers(request, cust_id):
    customer = get_object_or_404(Customer, pk=cust_id)
    customer.papers = not customer.papers
    customer.save()
    return HttpResponseRedirect(reverse_lazy('crm_api:index'))


@login_required
def download_file(request, file_id):
    cust_file = get_object_or_404(CustomerFiles, pk=file_id)
    file_name = str(cust_file.files)
    mime = mimetypes.guess_type(file_name)
    if mime[0] is None:
        mime = ('application/octet-stream', None)
    response = FileResponse(cust_file.files, content_type='file/%s' % mime[0].split('/')[1])
    response['Content-Disposition'] = "attachment;filename=%s" % file_name.split('/')[1]
    return response


@login_required
def select_customer(request):
    return render(request, 'crm_api/html/search_page.html')


@login_required
def settings_view(request):
    return render(request, 'crm_api/html/settings.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            return redirect(reverse_lazy('crm_api:index'))
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


@login_required
def create_folder(request, cust_id):
    if request.method == 'POST':
        print('folder name:', request.POST['folder_name'])
        if request.POST['folder_name']:
            try:
                cust = Customer.objects.get(pk=cust_id)
                folder_path = os.path.normpath(os.path.join('media/', 'user_{0}/{1}'.format(cust.name, request.POST['folder_name'])))
                os.makedirs(folder_path, exist_ok=True)
                messages.success(request, 'Adresář %s byl úspěšně vytvořen' % request.POST['folder_name'])
            except (Customer.DoesNotExist, FileExistsError, PermissionError):
                messages.error(request, 'Adresář nemohl být vytvořen')
    return redirect(reverse_lazy('crm_api:list_files', kwargs={'cust_id': cust_id}))


# Customer views starts here
class CustomerSearchList(LoginRequiredMixin, generic.ListView):
    model = Customer
    template_name = 'crm_api/html/customer_search_result.html'
    login_url = '/login/'
    paginate_by = PAGE_NUM

    def get_queryset(self):
        query_set = Customer.objects.all()
        search_query = self.request.GET.get('q', None)
        search_filter = self.request.GET.get('filter_papers', None)
        if search_query is not None:
            query_set = Customer.objects.filter(name__contains='%s' % search_query)
        if search_filter in ['yes', 'no']:
            query_set = query_set.filter(papers__exact=search_filter == 'yes')
        return query_set


class CustomerList(LoginRequiredMixin, generic.ListView):
    model = Customer
    template_name = 'crm_api/html/index.html'
    login_url = '/login/'
    paginate_by = PAGE_NUM


class CustomerCreateView(PermissionRequiredMixin, LoginRequiredMixin, generic.CreateView):
    permission_required = 'crm_api.add_customer'
    model = Customer
    success_url = reverse_lazy('crm_api:index')
    fields = '__all__'
    template_name = 'crm_api/html/create_subject.html'
    login_url = '/login/'

    def form_valid(self, form):
        try:
            os.mkdir(os.path.join(settings.MEDIA_ROOT, form.instance.name))
        except:
            messages.error(self.request, 'Chyba při vytváření klienta')
            return redirect(reverse_lazy('crm_api:index'))
        return super(CustomerCreateView, self).form_valid(form)


class CustomerUpdate(PermissionRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    permission_required = 'crm_api.change_customer'
    model = Customer
    template_name = 'crm_api/html/update_customer.html'
    fields = '__all__'
    success_url = reverse_lazy('crm_api:index')
    login_url = '/login/'


class CustomerDelete(PermissionRequiredMixin, LoginRequiredMixin, generic.DeleteView):
    permission_required = 'crm_api.delete_customer'
    model = Customer
    success_url = reverse_lazy('crm_api:index')
    fields = ['name']
    login_url = '/login/'


# Customer file views starts here
class CustomerFilesList(LoginRequiredMixin, generic.CreateView, generic.ListView):
    model = CustomerFiles
    fields = ['files']
    template_name = 'crm_api/html/file_list.html'
    login_url = '/login/'
    context_object_name = 'files'

    def _get_cust_dir(self):
        # print('url:', self.request.get_full_path())
        path_tmp = os.path.join(settings.MEDIA_ROOT, str(Customer.objects.get(pk=self.kwargs['cust_id'])))
        cust_dir = path_tmp
        if self.request.GET and 'dir' in self.request.GET:
            cust_dir = os.path.normpath(os.path.join(cust_dir, self.request.GET['dir']))
        if not cust_dir.startswith(path_tmp):
            cust_dir = path_tmp
        return cust_dir

    def _file_path(self, filename):
        try:
            cust_dir = self._get_cust_dir()
            file_path = os.path.normpath(os.path.join(cust_dir, filename))
            print('file_path:', file_path)
            if not file_path.startswith(cust_dir):
                return cust_dir
            return file_path
        except:
            print(sys.exc_info()[0])
            return None

    def get_queryset(self):
        try:
            cust_dir = self._get_cust_dir()
            file_list = []
            for x in os.listdir(cust_dir):
                file_list.append(CFile(os.path.join(cust_dir, x)))
            return file_list
        except:
            print(sys.exc_info()[0])
            return []        

    def form_valid(self, form):
        try:
            form.instance.customer = Customer.objects.get(pk=self.kwargs['cust_id'])
            print(form.instance.files, form.instance.files.path, os.path.exists(form.instance.files.path))

        except Customer.DoesNotExist:
            messages.error(self.request, 'Neplatný subjekt')
            return redirect(self.request.get_full_path())
        return super(CustomerFilesList, self).form_valid(form)

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Soubor úspěšně přidán')
        if isinstance(self.object, CustomerFiles):
            print(self.object.files.path)
            os.rename(self.object.files.path, self._file_path(self.object.filename()))
        return self.request.get_full_path()


class CustomerFilesDelete(PermissionRequiredMixin, LoginRequiredMixin, generic.DeleteView):
    permission_required = 'crm_api.delete_customerfiles'
    model = CustomerFiles
    fields = ['files']
    login_url = '/login/'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        print('trying to delete', os.path.join(settings.MEDIA_ROOT, str(obj.files)))
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, str(obj.files)))
        except OSError:
            pass
        return super(CustomerFilesDelete, self).delete(request, args, kwargs)

    def get_success_url(self, **kwargs):
        return self.request.get_full_path()
    

# Settings views starts here
class CustomPasswordChangeForm(PasswordChangeForm):
    error_css_class = 'has-error'
    error_messages = {'password_incorrect': 'Nespravne heslo',
                      'password_mismatch': 'Hesla se neshoduji'}
    old_password = forms.CharField(required=True, label='Staré heslo',
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                   error_messages={'required': 'Vyplňte toto pole'})
    new_password1 = forms.CharField(required=True, label='Nové heslo',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                    error_messages={'required': 'Vyplňte toto pole'})
    new_password2 = forms.CharField(required=True, label='Potvrďte nové heslo',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                    error_messages={'required': 'Vyplňte toto pole'})


#Warning email views starts here
class WarningEmailCreateView(PermissionRequiredMixin, LoginRequiredMixin, generic.CreateView):
    permission_required = 'crm_api.add_warningemail'
    model = WarningEmail
    success_url = reverse_lazy('crm_api:set_emails')
    fields = '__all__'
    template_name = 'crm_api/html/create_email.html'
    login_url = '/login/'


class WarningEmailUpdate(PermissionRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    permission_required = 'crm_api.change_warningemail'
    model = WarningEmail
    template_name = 'crm_api/html/update_email.html'
    fields = '__all__'
    success_url = reverse_lazy('crm_api:set_emails')
    login_url = '/login/'


class WarningEmailDelete(PermissionRequiredMixin, LoginRequiredMixin, generic.DeleteView):
    permission_required = 'crm_api.delete_warningemail'
    model = WarningEmail
    success_url = reverse_lazy('crm_api:set_emails')
    fields = ['name']
    login_url = '/login/'
