from django.urls import path
from . import views

urlpatterns = [
  path('products/',views.ProductList.as_view()),
  path('products/<int:pk>/',views.ProductDetail.as_view()),
  path('collections/',views.CollectionList.as_view()),
  path('collections/<int:pk>/',views.CollectionDetail.as_view())

]

# //as_view is a class method that returns a function that can be used as a view. It takes an optional actions argument that is a dictionary mapping HTTP methods to action names. The action names are the names of the methods on the viewset that will be called when the corresponding HTTP method is received. For example, the following code creates a view that will call the list method on the viewset when a GET request is received and the create method when a POST request is received: