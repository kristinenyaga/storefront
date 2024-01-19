from django.urls import path
from . import views
from rest_framework import routers
router=routers.SimpleRouter()

router.register('products',views.ProductViewSet)
router.register('collections',views.CollectionViewSet)
urlpatterns =router.urls

# //as_view is a class method that returns a function that can be used as a view. It takes an optional actions argument that is a dictionary mapping HTTP methods to action names. The action names are the names of the methods on the viewset that will be called when the corresponding HTTP method is received. For example, the following code creates a view that will call the list method on the viewset when a GET request is received and the create method when a POST request is received: