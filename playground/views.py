from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product,Customer,Collection,Order,OrderItem
from tags.models import TaggedItem
from django.db.models import Q
from django.db.models.aggregates import Count,Min,Avg,Max
from django.db import transaction
# Create your views here.
def say_hello(request):
  # query_set = Customer.objects.filter(email__contains='.com')
  # query_set = Collection.objects.filter(featured_product__isnull=True)
  # query_set=Product.objects.filter(inventory__lt=10)
  # query_set=Order.objects.filter(customer__id=1)
  # query_set=OrderItem.objects.filter(product__collection__id=3)
  # query_set=Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
  # query_set=Product.objects.prefetch_related('promotions').select_related('collection').all()
  # query_set=Order.objects.select_related("customer").all()
  # query_set=Order.objects.select_related("customer").prefetch_related("orderitem_set__product").all().order_by('-placed_at')[:5]
  # query_set1=OrderItem.objects.select_related("product").filter(order__in=query_set).values()

  # order_count=Order.objects.aggregate(Count('id'))
  # product1_sold=OrderItem.objects.filter(product__id=1).aggregate(Count('id'))
  # customer1=Order.objects.filter(customer__id=1).aggregate(Count('id'))
  # min_price=Product.objects.filter(collection_id=3).aggregate(min_price=Min('unit_price'))
  # avg_price=Product.objects.filter(collection__id=3).aggregate(
  #   avg_price=Avg('unit_price'),
  #   max_price=Max('unit_price')
  #   )

  # // annotate is used to add a new field to the result set

  # getting tagged items
  # tags=TaggedItem.objects.get_tags_for(Product,1)

  # inserting items into collection
  # collection=Collection.objects.create(title='Video_games',featured_product_id=1)
  # collection.id

  # updating items in collection
  # Collection.objects.filter(pk=11).update(featured_product_id=None)

  # deleting items from collection
  # Collection.objects.filter(pk__gt=10).delete()

  # transactions
  # with transaction.atomic():
  #   order=Order()
  #   order.customer_id=1
  #   order.save()

  #   item1=OrderItem()
  #   item1.order=order
  #   item1.product_id=1
  #   item1.quantity=2
  #   item1.unit_price=80.60
  #   item1.save()
  return render(request, "hello.html", {'name': 'Kris'})

  #  select_related() is used to fetch related objects in one go.
# filter() is used to filter the objects based on some condition.
