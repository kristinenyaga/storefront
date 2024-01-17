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
    return Response("ok")

@api_view()
def product_detail(request,id):
  # try:
  #   product = Product.objects.get(id=id)
  #   serializer = ProductSerializer(product)
  #   return Response(serializer.data)
  # except Product.DoesNotExist:
  #   return Response(status=404)
  product=get_object_or_404(Product,pk=id)
  seerializer = ProductSerializer(product)
  return Response(seerializer.data)

@api_view()
def collection_detail(request,pk):
  collection = get_object_or_404(Collection,pk=pk)
  serializer = CollectionSerializer(collection)
  return Response(serializer.data)