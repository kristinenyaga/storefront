from django.urls import path
from . import views
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from  django.urls.conf import include
from pprint import pprint
router=DefaultRouter()

router.register('customers',views.CustomerViewSet)
router.register('products',views.ProductViewSet,basename='product')
router.register('collections',views.CollectionViewSet)
router.register('carts',views.CartViewSet,basename='cart')

products_router=routers.NestedDefaultRouter(router,'products',lookup='product')
products_router.register('reviews',views.ReviewViewSet,basename='product-reviews')

cart_router = routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_router.register('cartitems',views.CartItemViewSet,basename='cart-items')
pprint(cart_router.urls)

urlpatterns=[
  path('',include(router.urls)),
  path('',include(products_router.urls)),
  path('',include(cart_router.urls))
]

# //as_view is a class method that returns a function that can be used as a view. It takes an optional actions argument that is a dictionary mapping HTTP methods to action names. The action names are the names of the methods on the viewset that will be called when the corresponding HTTP method is received. For example, the following code creates a view that will call the list method on the viewset when a GET request is received and the create method when a POST request is received: