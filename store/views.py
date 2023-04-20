from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Product

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

