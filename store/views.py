from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse, BadHeaderError
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import re

from config import settings
from .models import Product, Order, Profile, OrderItem, Comment, Category
from .cart import Cart
from .forms import AddProductToCartForm, OrderCreateForm, ProfileForm, AddProductForm, CommentCreateForm
from like.models import Like


# Create your views here.


# def home_view(request):
#     return render(request, template_name='store/product_list.html')


class ProductList(generic.ListView):
    queryset = Product.objects.available().order_by('-date_time_created')
    template_name = 'store/product_list.html'
    context_object_name = 'products'
    paginate_by = 4


class ProductDetail(generic.DetailView):
    model = Product
    template_name = 'store/product_detail.html'

    def get_object(self, queryset=None):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_product_to_cart_form'] = AddProductToCartForm()
        product = self.get_object()
        if Like.objects.filter(user=self.request.user, object_id=product.pk).exists():
            context['like'] = 'unlike'
        else:
            context['like'] = 'like'
        return context


class ProductListPerCategory(generic.ListView):
    template_name = 'store/category.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        category = get_object_or_404(Category, title=self.kwargs.get('title'))
        return category.product_set.available().order_by('-date_time_created')


class CartView(TemplateView):
    template_name = 'store/cart_list.html'


def add_product_to_cart(request, pk):
    form = AddProductToCartForm(request.POST)
    if form.is_valid():
        quantity = form.cleaned_data.get('quantity', 0)
        product = get_object_or_404(Product, pk=pk)
        cart = Cart(request)
        cart.add_product(product, quantity)
        messages.success(request, f"{quantity} {product.title} added to the cart")
    return redirect('cart-list')


def add_product_to_cart_from_product_list_page(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = Cart(request)
    cart.add_product(product=product, quantity=1)
    messages.success(request, f"{1} {product.title} added to the cart")
    return redirect('cart-list')


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    messages.error(request, 'you cleared the cart')    
    return redirect('cart-list')


def remove_from_cart(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    cart.remove_product(product=product)
    messages.error(request, f"{product.title} has been removed")
    return redirect('cart-list')


@login_required
def create_order(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'your cart is empty please choose some products')
        return redirect('product-list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            try:
                send_mail('order created',
                          f"you have new order please check the admin panel",
                          "amirhosseing983@gmail.com", [f"{settings.ADMIN_EMAIL}"])
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            return redirect('product-list')
    elif request.method == "GET":
        if Order.objects.filter(profile__user=request.user).exists():
            profile = get_object_or_404(Profile, user=request.user)
            form = OrderCreateForm(initial=
            {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'phone_number': profile.phone_number,
                'address': profile.address,
            },
                request=request
        )
        else:
            form = OrderCreateForm(request=request, initial={'email': request.user.email})
    return render(request, 'store/checkout.html', context={'form': form})


@login_required
def update_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "GET":
        form = ProfileForm(request=request, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone_number': profile.phone_number,
            'address': profile.address,
        })
    else:
        form = ProfileForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect('product-list')

    return render(request, 'store/profile_update.html',  context={'form': form})


@login_required
def like_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if Like.objects.filter(user=request.user, object_id=pk):
        Like.objects.filter(user=request.user, object_id=product.pk).delete()
        messages.error(request, 'product unliked')
    else:
        product.likes.create(user=request.user)
        messages.success(request, 'product liked')

    return redirect('product-detail', slug=product.slug)


@login_required
def product_liked_list(request):
    likes = Like.objects.filter(user=request.user).values('object_id')
    products = Product.objects.available().filter(id__in=likes)
    return render(request, template_name='store/product_liked.html', context={'products': products})


class OrderView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'orders'
    template_name = 'store/order.html'

    def get_queryset(self):
        return Order.objects.filter(profile__user=self.request.user)


def persian_slugify(text):
    """
    Converts Persian text to a slug for use in URLs.
    """
    # text = re.sub('[^\w\s-]', '', text).strip().lower()
    # text = re.sub('[-\s]+', '-', text)
    text = '-'.join(text.split())
    return text


class ProductCreate(UserPassesTestMixin, generic.CreateView):
    model = Product
    template_name = 'store/product_add.html'
    form_class = AddProductForm

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        if form.is_valid():
            product = form.save(commit=False)
            product.slug = persian_slugify(product.title)
            product.save()
            return super().form_valid(form)


class CommentCreate(LoginRequiredMixin, generic.CreateView):
    model = Comment
    form_class = CommentCreateForm
    template_name = 'store/product_detail.html'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.product = get_object_or_404(Product, pk=self.kwargs['pk'])
        comment.user = self.request.user
        comment.save()
        try:
            send_mail('comment created', f"new comment is added for {comment.product.title} please check the content so it can be display", "amirhosseing983@gmail.com", [f"{settings.ADMIN_EMAIL}"])
        except BadHeaderError:
            return HttpResponse("Invalid header found.")
        return super().form_valid(form)


class CommentDelete(UserPassesTestMixin, LoginRequiredMixin, generic.DeleteView):
    model = Comment
    template_name = 'store/comment_delete_confrim.html'

    def test_func(self):
        return bool(self.get_object().user == self.request.user)

    def get_success_url(self):
        return reverse_lazy('product-detail', args=[self.kwargs['product_slug']])


