from django.conf.urls import url

from . import views


app_name = 'crm_api'
urlpatterns = [
    url(r'^$', views.customer_form, name='create_customer'),
    url(r'^thanks/$', views.thanks, name='thanks'),
]