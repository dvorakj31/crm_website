from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


app_name = 'crm_api'
urlpatterns = [
    url(r'^$', views.CustomerList.as_view(), name='index'),
    url(r'^create_client/$', views.CustomerCreateView.as_view(), name='create_customer'),
    url(r'^update_client/(?P<pk>[0-9]+)/$', views.CustomerUpdate.as_view(), name='edit'),
    url(r'^delete_client/(?P<pk>[0-9]+)/$', views.CustomerDelete.as_view(), name='delete_customer'),
    url(r'^list_files/(?P<cust_id>[0-9]+)/$', views.CustomerFilesList.as_view(), name='list_files'),
    url(r'^add_file/(?P<cust_id>[0-9]+)/$', views.CustomerFilesCreateView.as_view(), name='add_file'),
    url(r'^delete_file/(?P<pk>[0-9]+)/$', views.CustomerFilesDelete.as_view(), name='delete_file'),
    url(r'^edit_papers/(?P<cust_id>[0-9]+)/$', views.edit_papers, name='edit_papers'),
    url(r'^login/$', auth_views.login, {'template_name': 'crm_api/html/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/crm'}, name='logout'),
]
