from django.urls import path
from . import views

urlpatterns = [
  path('products/',views.products),
  path('products/<int:id>/',views.product_detail),
  path('collections/<int:pk>/',views.collection_detail,name='collection-detail')

]