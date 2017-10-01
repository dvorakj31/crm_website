from django.conf.urls import url

from . import views


app_name = 'crm_api'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_client/$', views.customer_form, name='create_customer'),
    url(r'^thanks/$', views.thanks, name='thanks'),
    url(r'^edit/$', views.EditListView.as_view(), name='edit'),
]