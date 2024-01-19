from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from .models import Product,Collection,OrderItem
from .serializers import ProductSerializer,CollectionSerializer
# Create your views here.

class ProductViewSet(ModelViewSet):
  queryset=Product.objects.select_related('collection').all()
  serializer_class=ProductSerializer

  def destroy(self, request, *args, **kwargs):
    if OrderItem.objects.filter(product_id=kwargs['pk']).count()>0:
      return Response({'error':'The product cannot be deleted as it has an associated order item'},status=401)
    return super().destroy(request, *args, **kwargs)

    
class CollectionViewSet(ModelViewSet):
  queryset=Collection.objects.all()
  serializer_class=CollectionSerializer

  def destroy(self, request, *args, **kwargs):
    if Product.objects.filter(collection_id=kwargs['pk']).count()>0:
      return Response({'error':'The collection cannot be deleted as it has associated products'},status=401)
    return super().destroy(request, *args, **kwargs)
  


class ProductList(ListCreateAPIView):
  queryset=Product.objects.select_related('collection').all()
  serializer_class=ProductSerializer

class ProductDetail(RetrieveUpdateDestroyAPIView):
  queryset=Product.objects.select_related('collection').all()
  serializer_class=ProductSerializer

  def delete(self,pk):
    product=get_object_or_404(Product,pk=pk)
    if product.orderitems.count()>0:
      return Response({'error':'The product cannot be deleted as it has an associated order item'},status=401)
    else:
      product.delete()
      return Response(status=204)

class CollectionDetail(RetrieveUpdateDestroyAPIView):
  queryset=Collection.objects.all()
  serializer_class=CollectionSerializer
  
  def delete(self,pk):
    collection=get_object_or_404(Collection,pk=pk)
    if collection.products.count()>0:
      return Response({'error':'The collection cannot be deleted as it has associated products'},status=401)
    else:
      collection.delete()
      return Response(status=204)
  
class CollectionList(ListCreateAPIView):
  queryset=Collection.objects.all()
  serializer_class=CollectionSerializer

  
