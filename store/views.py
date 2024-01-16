from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

@api_view()
def products(request):
  return Response("ok")

@api_view()
def product_detail(request,id):
  return Response(id)