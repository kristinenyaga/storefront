from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product,Collection
from .serializers import ProductSerializer,CollectionSerializer
# Create your views here.

@api_view(['GET','POST'])
def products(request):
  if request.method == 'GET':
    products=Product.objects.select_related('collection').all()
    serializer=ProductSerializer(products,many=True,context={'request':request})
    return Response(serializer.data)
  
  elif request.method == 'POST':
    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data,status=201)

@api_view(['GET','PUT','PATCH','DELETE'])
def product_detail(request,id):
  # try:
  #   product = Product.objects.get(id=id)
  #   serializer = ProductSerializer(product)
  #   return Response(serializer.data)
  # except Product.DoesNotExist:
  #   return Response(status=404)
  product=get_object_or_404(Product,pk=id)
  if request.method == 'GET':
    serializer = ProductSerializer(product)
    return Response(serializer.data,status=200)
  elif request.method == 'PUT':
    serializer = ProductSerializer(product,data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data,status=200)
  elif request.method == 'DELETE':
    if product.orderitems.count()>0:
      return Response({'error':'The product cannot be deleted as it has an associated order item'},status=401)
    else:
      product.delete()
      return Response(status=204)

@api_view()
def collection_detail(request,pk):
  collection = get_object_or_404(Collection,pk=pk)
  serializer = CollectionSerializer(collection)
  return Response(serializer.data)