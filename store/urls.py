from django.urls import path, include
from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view(), name='product-list')
   ]