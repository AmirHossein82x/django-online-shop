from .cart import Cart


def cart_processor(request):
    cart = Cart(request)
    return {'cart': cart}
