from django.db import models
from tastypie.resources import ModelResource
from cities.models import City


class CityResource(ModelResource):
    class Meta:
        queryset = City.objects.all()
        resource_name = 'cities'
        excludes = ['id', 'date_created']
