from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser,IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.decorators import action
from .models import Product,Collection,OrderItem,Review,Cart,CartItem,Customer,Order
from .serializers import CustomerSerializer, ProductSerializer,CollectionSerializer,ReviewSerializer,CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer,OrderSerializer,CreateOrderSerializer,UpdateOrderSerializer
from .filters import ProductFilter  

from .permissions import IsAdminOrReadOnly,CanViewHistory
# Create your views here.
class CustomerViewSet(ModelViewSet):
  queryset=Customer.objects.all()
  serializer_class = CustomerSerializer
  # permission_classes = [IsAdminUser]

  # def get_permissions(self):
  #   if self.request.method == 'GET':
  #     return [AllowAny()]
  #   return [IsAuthenticated()]
  
  # //get_permissions is a method that returns a list of permission instances that this view requires.

  @action(detail=False,methods=['GET','PUT','PATCH'],permission_classes=[IsAuthenticated])
  def me(self,request):
    customer = Customer.objects.get(user_id=request.user.id)
    if request.method == 'GET':
      serializer=CustomerSerializer(customer)
      return Response(serializer.data)
  
    elif request.method == 'PUT':
      serializer=CustomerSerializer(customer,data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response(serializer.data)
  
  @action(detail=True,methods=['GET'],permission_classes=[CanViewHistory])
  def history(self,request,pk):
    return Response("ok")


class ProductViewSet(ModelViewSet):
  serializer_class=ProductSerializer
  queryset=Product.objects.all()
  permission_classes=[IsAdminOrReadOnly]

  filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
  filterset_class=ProductFilter
  search_fields=['title','description'] 
  ordering_fields=['unit_price','last_update'] 
  pagination_class=PageNumberPagination
  permission_classes=[IsAdminOrReadOnly]
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
  permission_classes=[IsAdminOrReadOnly]

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
  
class OrderViewSet(ModelViewSet):
  http_method_names=['get','patch','options','head','delete']
  def get_permissions(self):
    if self.request.method in ['PATCH','DELETE']:
      return [IsAdminUser()]
    return [IsAuthenticated()]

  def get_serializer_class(self):
    if self.request.method == 'POST':
      return CreateOrderSerializer
    elif self.request.method == 'PATCH':
      return UpdateOrderSerializer
    return OrderSerializer


  def get_queryset(self):
    user=self.request.user
    if user.is_staff:
      return Order.objects.all()  
    customer=Customer.objects.only('id').get(user_id=user.id)
    return Order.objects.filter(customer_id=customer)
  
  def create(self, request, *args, **kwargs):
    serializer = CreateOrderSerializer(data=request.data,context={'user_id':self.request.user.id})
    serializer.is_valid(raise_exception=True)
    order=serializer.save()
    order_serializer=OrderSerializer(order)
    return Response(
      {"order": order_serializer.data, "cart_id": serializer.validated_data.get("cart_id")},
      status=201
        )

    

  # def get_queryset(self):
  #   return super().get_queryset()