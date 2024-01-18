from rest_framework import serializers
from rest_framework.relations import HyperlinkedRelatedField
from decimal import Decimal
from .models import Collection, Product
class CollectionSerializer(serializers.ModelSerializer):
  product_count= serializers.SerializerMethodField(method_name='get_product_count')
  class Meta:
    model=Collection
    fields=['id','title','product_count']

  def get_product_count(self,collection):
    return collection.products.count()

class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = ['id','title','slug','description','unit_price','price_with_tax','collection']
  # id = serializers.IntegerField()
  # title = serializers.CharField(max_length=255)
  # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
  price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
  # collection = HyperlinkedRelatedField(
  #   queryset=Collection.objects.all(),
  #   view_name='collection-detail'
  # )
  

  def calculate_tax(self, product):
    return product.unit_price * Decimal(1.1)
