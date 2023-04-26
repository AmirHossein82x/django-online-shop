from .cart import Cart
from .models import Category


def cart_processor(request):
    cart = Cart(request)
    return {'cart': cart}


def category_processor(request):
    query = Category.objects.all()
    return {'categories': query}