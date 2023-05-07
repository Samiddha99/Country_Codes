from django.contrib import admin
from .models import *


# Register your models here.
class countryDataAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'dial_code', 'flag']
admin.site.register(Country_Code, countryDataAdmin)