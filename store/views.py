from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product,Collection
from .serializers import ProductSerializer,CollectionSerializer
# Create your views here.


class ProductList(APIView):
  def get(self,request):
    products=Product.objects.select_related('collection').all()
    serializer=ProductSerializer(products,many=True,context={'request':request})
    return Response(serializer.data)
  
  def post(self,request):
    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data,status=201)

class ProductDetail(APIView):
  # try:
  #   product = Product.objects.get(id=id)
  #   serializer = ProductSerializer(product)
  #   return Response(serializer.data)
  # except Product.DoesNotExist:
  #   return Response(status=404)
  def get(self,request,id):
    product=get_object_or_404(Product,pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data,status=200)
  def put(self,request,id):
    product=get_object_or_404(Product,pk=id)
    serializer = ProductSerializer(product,data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data,status=200)
  def delete(self,request,id):
    product=get_object_or_404(Product,pk=id)
    if product.orderitems.count()>0:
      return Response({'error':'The product cannot be deleted as it has an associated order item'},status=401)
    else:
      product.delete()
      return Response(status=204)

class CollectionDetail(APIView):
  def get(self,request,pk):
    collection = get_object_or_404(Collection,pk=pk)
    serializer = CollectionSerializer(collection)
    return Response(serializer.data,status=200)
  
  def put(self,request,pk):
    collection = get_object_or_404(Collection,pk=pk)
    serializer = CollectionSerializer(collection,data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data,status=200)
  
  def delete(self,request,pk):
    collection=get_object_or_404(Collection,pk=pk)
    if collection.products.count()>0:
      return Response({'error':'The collection cannot be deleted as it has associated products'},status=401)
    else:
      collection.delete()
      return Response(status=204)
  
class CollectionList(APIView):
  def get(self,request):
    collections=Collection.objects.all()
    serializer=CollectionSerializer(collections,many=True)
    return Response(serializer.data)
  
  def post(self,request):
    serializer = CollectionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data,status=201)
  
