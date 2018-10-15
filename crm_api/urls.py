from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'crm_api'
urlpatterns = [
    path('', views.CustomerList.as_view(), name='index'),
    path('create_client/', views.CustomerCreateView.as_view(), name='create_customer'),
    path('update_client/<int:pk>/', views.CustomerUpdate.as_view(), name='edit'),
    path('delete_client/<int:pk>/', views.CustomerDelete.as_view(), name='delete_customer'),
    path('search_customer/', views.select_customer, name='select_customer'),
    path('result/', views.CustomerList.as_view(), name='customer_search_result'),
    path('list_files/<int:cust_id>/', views.CustomerFilesList.as_view(), name='list_files'),
    path('delete_file/<int:pk>/', views.CustomerFilesDelete.as_view(), name='delete_file'),
    path('download_file/<int:file_id>/', views.download_file, name='download_file'),
    path('create_folder/<int:cust_id>/', views.create_folder, name='create_folder'),
    re_path(r'^delete_folder/(?P<path>.*)/$', views.delete_folder, name='delete_folder'),
    path('edit_papers/<int:cust_id>/', views.edit_papers, name='edit_papers'),
    path('edit_tax_submit/<int:cust_id>/', views.edit_tax_submit, name='edit_tax_submit'),
    path('change_password/', views.change_password, name='change_password'),
    path('set_emails/', views.set_emails, name='set_emails'),
    path('create_email/', views.WarningEmailCreateView.as_view(), name='create_email'),
    path('edit_email/<int:pk>/', views.WarningEmailUpdate.as_view(), name='edit_email'),
    path('delete_email/<int:pk>/', views.WarningEmailDelete.as_view(), name='delete_email'),
    path('login/', auth_views.LoginView.as_view(template_name='crm_api/html/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=''), name='logout'),
]
