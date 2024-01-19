from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .models import Product,Collection,OrderItem,Review
from .serializers import ProductSerializer,CollectionSerializer,ReviewSerializer
from .filters import ProductFilter  # Import the ProductFilter class

# Create your views here.

class ProductViewSet(ModelViewSet):
  serializer_class=ProductSerializer
  queryset=Product.objects.all()

  filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
  filterset_class=ProductFilter
  search_fields=['title','description'] 
  ordering_fields=['unit_price','last_update'] 
  pagination_class=PageNumberPagination
  # def get_queryset(self):
  #   queryset=Product.objects.all()
  #   collection_id = self.request.query_params.get('collection_id')
  #   if collection_id is not None:
  #     queryset=queryset.filter(collection_id=collection_id)
    
  #   return queryset
  def get_serializer_context(self):
    return {'request':self.request}


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



  
