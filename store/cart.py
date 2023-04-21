from store.models import Product


class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.cart = self.session.get('cart')
        if not self.cart:
            self.cart = self.session['cart'] = {}

    def save(self):
        self.session.modified = True

    def add_product(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity}
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove_product(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session['cart']
        self.save()

    def __iter__(self):
        cart = self.cart.copy()
        product_ids = list(map(int, self.cart.keys()))
        for product in Product.objects.filter(id__in=product_ids):
            cart[str(product.id)]['obj'] = product
            cart[str(product.id)]['price'] = product.final_price() * cart[str(product.id)]['quantity']

        for item in cart.values():
            yield item

    def total_price(self):
        total = 0
        product_ids = list(map(int, self.cart.keys()))
        for product in Product.objects.filter(id__in=product_ids):
            quantity = self.cart[str(product.id)]['quantity']
            total += product.final_price() * quantity
        return total

    def __len__(self):
        return len(self.cart.keys())







