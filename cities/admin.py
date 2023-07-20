from django.contrib import admin
from .models import City
# Register your models here.


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'date_created')
    list_filter = ('name', 'price')
    search_fields = ('name', 'price')


admin.site.register(City, CityAdmin)
