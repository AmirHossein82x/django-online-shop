from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.contenttypes.admin import GenericStackedInline
from django.db import models
from .models import Product, Category, Promotion, Profile, OrderItem, Order
from like.models import Like


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ['title__istartswith']


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('discount',)


class ProductFilter(admin.SimpleListFilter):
    title = 'available'
    parameter_name = 'available'

    def lookups(self, request, model_admin):
        return [
            ("all", "all products"),
            ("available", "just available products"),
        ]
    
    def queryset(self, request, queryset):
        if self.value() == 'all':
            return queryset.filter(quantity__gt=0)
        elif self.value() == 'available':
            return queryset.all()


class LikeInline(GenericStackedInline):
    model = Like
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_category', 'quantity', 'price', 'discount', 'final_price')
    list_editable = ('quantity',)
    list_filter = ('category', ProductFilter)
    list_per_page = 10
    search_fields = ['title__istartswith']
    autocomplete_fields = ('category',)
    inlines = [LikeInline]

    prepopulated_fields = {
        'slug': ('title',)
    }
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple('verbose name', False)}
    }

    def get_category(self, product):
        return ', '.join([item.title for item in product.category.all()])

    def discount(self, product):
        if product.promotion:
            return f"{int((product.promotion.discount) * 100)}%"
        return 0

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('promotion')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'phone_number')

    def user_name(self, profile):
        return profile.user.username

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ('product', 'quantity', 'price')
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('username', 'created', 'address', 'is_send')
    inlines = [OrderItemInline]
    actions = ['send_order']

    @admin.action(description="Mark selected orders that send to the customer")
    def send_order(self, request, queryset):
        number = queryset.update(is_send=True)
        self.message_user(
            request,
            f"{number} orders send "
        )

    def username(self, order):
        return order.profile.user.username

    def address(self, order):
        return order.profile.address

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('profile')