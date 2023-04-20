from django.shortcuts import render
from django.views import generic
from .models import Product

# Create your views here.


# def home_view(request):
#     return render(request, template_name='store/product_list.html')


class ProductList(generic.ListView):
    template_name = 'store/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.available()
