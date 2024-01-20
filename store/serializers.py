from rest_framework import serializers
from rest_framework.relations import HyperlinkedRelatedField
from decimal import Decimal
from .models import Collection, Product, Review,Cart,CartItem
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

class ReviewSerializer(serializers.ModelSerializer):
  class Meta:
    model=Review
    fields=['id','date','name','description']

  def create(self, validated_data):
    product_id=self.content['product_id']
    return Review.objects.create(product_id=product_id,**validated_data)
  
  # // validated data is a dictionary containing the data that was passed to the serializer. It is validated by the serializer before being passed to the create method.
class SimpleProductSerializer(serializers.ModelSerializer):
  class Meta:
    model=Product
    fields=['id','title','description','unit_price']
class CartItemSerializer(serializers.ModelSerializer):
  product=SimpleProductSerializer(read_only=True)
  total_price=serializers.SerializerMethodField(method_name='get_total_price')

  def get_total_price(self,cart_item):
    return cart_item.product.unit_price * cart_item.quantity

  class Meta:
    model=CartItem
    fields=['id','product','quantity','total_price']
class CartSerializer(serializers.ModelSerializer):
  id=serializers.UUIDField(read_only=True)
  items=CartItemSerializer(many=True,read_only=True)
  total_price=serializers.SerializerMethodField(method_name='get_total_price')

  def get_total_price(self,cart):
    # total =0
    # for items in cart.items.all():
    #   total+=items.product.unit_price*items.quantity
    # return total
    return sum([item.quantity * item.product.unit_price for item in cart.items.all()])


  class Meta:
    model=Cart
    fields=['id','created_at','items','total_price']

class AddCartItemSerializer(serializers.ModelSerializer):
  product_id=serializers.IntegerField()

  def validate_product_id(self,value):
    if not Product.objects.filter(pk=value).exists():
      raise serializers.ValidationError('The product with the given id doesnt exist')
    return value

  def save(self, **kwargs):
    product_id=self.validated_data['product_id']
    quantity=self.validated_data['quantity']
    cart_id = self.context['cart_id']
    
    try:
      cart_item=CartItem.objects.get(cart_id=cart_id,product_id=product_id)
      # update item
      cart_item.quantity +=quantity
      cart_item.save()
      self.instance=cart_item
    except CartItem.DoesNotExist:
      # create new item
      self.instance=CartItem.objects.create(cart_id=cart_id,**self.validated_data)

    return self.instance
  class Meta:
    model = CartItem
    fields=['product_id','quantity']

class UpdateCartItemSerializer(serializers.ModelSerializer):
  class Meta:
    model=CartItem
    fields=['quantity']
