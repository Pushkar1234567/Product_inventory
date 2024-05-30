from django.urls import path
from .views import CreateProduct,ProductRetrieveUpdateDestroy

urlpatterns = [
    path('product/',CreateProduct.as_view(), name='product list create' ),
    path('product/<int:pk>/',ProductRetrieveUpdateDestroy.as_view(), name='product Retrieve Update Delete' ),
]