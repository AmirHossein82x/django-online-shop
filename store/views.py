from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.views import generic
from .models import Product
from .cart import Cart
from .forms import AddProductToCartForm

# Create your views here.


# def home_view(request):
#     return render(request, template_name='store/product_list.html')


class ProductList(generic.ListView):
    template_name = 'store/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        if query_param := self.request.GET.get('category__title'):
            return Product.objects.available().filter(category__title__exact=query_param)
        return Product.objects.available()


class ProductDetail(generic.DetailView):
    model = Product
    template_name = 'store/product_detail.html'

    def get_object(self, queryset=None):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_product_to_cart_form'] = AddProductToCartForm()
        return context


class CartView(TemplateView):
    template_name = 'store/cart_list.html'


def add_product_to_cart(request, pk):
    form = AddProductToCartForm(request.POST)
    if form.is_valid():
        quantity = form.cleaned_data.get('quantity', 0)
        product = get_object_or_404(Product, pk=pk)
        cart = Cart(request)
        cart.add_product(product, quantity)
    return redirect('cart-list')


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart-list')

