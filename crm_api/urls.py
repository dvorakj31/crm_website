from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


app_name = 'crm_api'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_client/$', views.CustomerCreateView.as_view(), name='create_customer'),
    url(r'^select_customer/$', views.select_customer, name='select_customer'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.CustomerUpdate.as_view(), name='edit'),
    url(r'^delete/$', views.delete_customer, name='delete'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.CustomerDelete.as_view(), name='delete_customer'),
    url(r'^login/$', auth_views.login, {'template_name': 'crm_api/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'crm_api/logout.html', 'next_page': '/crm'}, name='logout'),
]
