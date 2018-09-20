from django.contrib import admin

# Register your models here.
from crm_api.models import Customer, CustomerFiles

admin.site.register(Customer)
admin.site.register(CustomerFiles)