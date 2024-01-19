# filters.py
from django_filters import rest_framework as filters
from .models import Product

class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'unit_price': ['lt', 'gt'],
            'collection_id': ['exact'],
        }
