from django.conf.urls import url

from . import views


app_name = 'crm_api'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_client/$', views.customer_form, name='create_customer'),
    url(r'^thanks/$', views.thanks, name='thanks'),
    url(r'^select_customer/$', views.SelectCustomerListView.as_view(), name='select_customer'),
    url(r'^(?P<pk>[0-9]+)/$', views.CustomerUpdate.as_view(), name='edit_customer'),
]
