from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .models import Product,Collection,OrderItem,Review,Cart,CartItem,Customer
from .serializers import CustomerSerializer, ProductSerializer,CollectionSerializer,ReviewSerializer,CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer
from .filters import ProductFilter  # Import the ProductFilter class

# Create your views here.
class CustomerViewSet(CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,GenericViewSet):
  queryset=Customer.objects.all()
  serializer_class = CustomerSerializer

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


class CartViewSet(CreateModelMixin,RetrieveModelMixin,GenericViewSet,DestroyModelMixin):
  queryset=Cart.objects.prefetch_related('items__product').all()
  serializer_class=CartSerializer

class CartItemViewSet(ModelViewSet):
  http_method_names=['get','post','patch','delete']
  def get_queryset(self):
    return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])
  
  def get_serializer_class(self):
    if self.request.method == 'POST':
      return AddCartItemSerializer
    elif self.request.method == 'PATCH':  
      return UpdateCartItemSerializer
    return CartItemSerializer
  
  def get_serializer_context(self):
    return {'cart_id':self.kwargs['cart_pk']}