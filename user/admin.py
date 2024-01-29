from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

# Register your models here.

@admin.register(User)
class UsersAdmin(ImportExportModelAdmin):
    list_display = ('username', 'first_name', 'last_name','email',
                    'is_marketer', 'is_accountant', 'is_admin',)
    search_fields = ['username', 'first_name', 'last_name']
    list_editable = ['is_marketer', 'is_accountant', 'is_admin',]
    list_filter = ('is_marketer', 'is_accountant', 'is_admin',)
