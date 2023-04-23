from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models
from .models import Product, Category, Promotion, Profile, OrderItem, Order


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ['title__istartswith']



@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('discount',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_category', 'quantity', 'price', 'discount', 'final_price')
    list_editable = ('quantity',)
    list_filter = ('category',)
    list_per_page = 10
    search_fields = ['title__istartswith']
    autocomplete_fields = ('category',)
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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('username', 'created')
    inlines = [OrderItemInline]

    def username(self, order):
        return order.profile.user.username
