from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from .models import Product,Collection,OrderItem,Review
from .serializers import ProductSerializer,CollectionSerializer,ReviewSerializer
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
  
class ReviewViewSet(ModelViewSet):
  def get_queryset(self):
    return Review.objects.filter(product_id=self.kwargs['product_pk'])
  
  serializer_class = ReviewSerializer

  def get_serializer_context(self):
    return {'product_id':self.kwargs['product_pk']}



  
