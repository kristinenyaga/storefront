from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.db.models import Count, F
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models
# Register your models here.
class InventoryFilter(admin.SimpleListFilter):
  title='inventory'
  # //title is used to specify the title of the filter that will be displayed in the sidebar.
  parameter_name='inventory'
  # // parameter_name is used to specify the name of the query string parameter that will be used to filter the results.
  def lookups(self, request, model_admin) -> list[tuple[Any, str]]:
    return [
      ('<10','Low'),
    ]
  def queryset(self, request, queryset: QuerySet):
    if self.value() == '<10':
      return queryset.filter(inventory__lt=10)


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
  list_display=['title','products_count']
  search_fields=['title']

  def products_count(self,collection):
    url=(reverse('admin:store_product_changelist')
         +'?'
         +urlencode({'collection__id':str(collection.id)}))
    return format_html('<a href="{}">{}</a>',url,collection.products_count)
  

  def get_queryset(self, request: HttpRequest) -> QuerySet:
    return super().get_queryset(request).annotate(
      products_count=Count('products')
    )
  
  # // get_queryset is used to customize the queryset that is used to populate the list of collections in the admin interface. By default, it returns all collections.

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
  actions=['add_price']
  list_display=['title','unit_price','inventory_status','collection']
  list_editable=['unit_price']
  list_per_page=10
  list_select_related=['collection']
  list_filter=['collection','last_update',InventoryFilter]
  prepopulated_fields={'slug':['title']}
  autocomplete_fields=['collection']
  search_fields=['title']


  @admin.display(ordering='inventory')
  def inventory_status(self,product):
    if product.inventory < 10:
      return 'Low'
    return 'Ok'
  
  @admin.action(description='add price')
  def add_price(self,request,queryset):
    # // queryset is the list of products that were selected in the changelist page.
    # // request is the HttpRequest object for the current request.

    queryset.update(unit_price=F('unit_price')+10)
    self.message_user(request,'price added successfully')


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
  list_display=['first_name','last_name','membership','orders_count']
  list_editable=['membership']
  list_per_page=10
  list_select_related =['user']
  ordering=['user__first_name','user__last_name']
  search_fields=['first_name__istartswith','last_name__istartswith']

  def orders_count(self,customer):
    url=(reverse('admin:store_order_changelist')
                +'?'
                +urlencode({'customer__id':str(customer.id)}))
    return format_html('<a href="{}">{}</a>',url,customer.orders_count)
  
  def get_queryset(self, request: HttpRequest) -> QuerySet:
    return super().get_queryset(request).annotate(
      orders_count=Count('order')
    
    )

class OrderItemInline(admin.TabularInline):
  model=models.OrderItem
  autocomplete_fields=['product']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
  list_display=['id','placed_at','customer']
  list_per_page=10
  ordering=['placed_at']
  autocomplete_fields=['customer']
  inlines=[OrderItemInline]
  # list_select_related=['customer']
  
  