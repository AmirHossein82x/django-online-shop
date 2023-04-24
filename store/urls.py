from django.urls import path, include
from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('products/<slug:slug>/', views.ProductDetail.as_view(), name='product-detail'),
    path('cart/view/', views.CartView.as_view(), name='cart-list'),
    path('cart/add/<int:pk>/', views.add_product_to_cart, name='add-product-to-cart'),
    path('cart/clear', views.clear_cart, name='clear-cart'),
    path('cart/delete/<int:pk>', views.remove_from_cart, name='cart-del-product'),
    path('checkout/', views.create_order, name='checkout'),
    path('profile/', views.update_profile, name='profile'),
]
