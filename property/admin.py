from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

# Register your models here.


@admin.register(Property)
class PropertyAdmin(ImportExportModelAdmin):
    list_display = ('name', 'status', 'value', 'type', )


@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin):
    list_display = ('full_name', 'address', 'email',
                    'phone_number', 'whatsapp', )
    search_fields = ['full_name', 'address',
                     'email', 'phone_number', 'whatsapp', ]


@admin.register(Prospect)
class ProspectAdmin(ImportExportModelAdmin):
    list_display = ('full_name', 'address', 'email',
                    'phone_number', 'whatsapp', 'status')
    search_fields = ['full_name', 'address', 'email',
                     'phone_number', 'whatsapp', 'status']
    list_filter = ('status',)
