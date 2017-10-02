from django.conf.urls import url

from . import views


app_name = 'crm_api'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_client/$', views.CustomerCreateView.as_view(), name='create_customer'),
    url(r'^thanks/$', views.thanks, name='thanks'),
    url(r'^select_customer/$', views.select_customer, name='select_customer'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.CustomerUpdate.as_view(), name='edit'),
    url(r'^delete/$', views.delete_customer, name='delete'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.CustomerDelete.as_view(), name='delete_customer'),
]
