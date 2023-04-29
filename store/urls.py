from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view(), name='product-list'),
    # path('products/<slug:slug>/', views.ProductDetail.as_view(), name='product-detail'),
    re_path('products/(?P<slug>[-\w]+)/', views.ProductDetail.as_view(), name='product-detail'),
    path('cart/view/', views.CartView.as_view(), name='cart-list'),
    path('cart/add/<int:pk>/', views.add_product_to_cart, name='add-product-to-cart'),
    path('cart/add/list/<int:pk>/', views.add_product_to_cart_from_product_list_page, name='add-product-to-cart-list'),
    path('cart/clear', views.clear_cart, name='clear-cart'),
    path('cart/delete/<int:pk>', views.remove_from_cart, name='cart-del-product'),
    path('checkout/', views.create_order, name='checkout'),
    path('profile/', views.update_profile, name='profile'),
    path('like/<int:pk>/', views.like_product, name='like-product'),
    path('likes/products/', views.product_liked_list, name='product-liked-list'),
    path('orders/', views.OrderView.as_view(), name='orders'),
    path('product/create/', views.ProductCreate.as_view(), name='add-product'),
    path('product/<int:pk>/comment/create/', views.CommentCreate.as_view(), name='create-comment'),
    path('product/<slug:product_slug>/comment/delete/<int:pk>/', views.CommentDelete.as_view(), name='comment-delete'),
    path('category/<str:title>/', views.ProductListPerCategory.as_view(), name='category'),

]
