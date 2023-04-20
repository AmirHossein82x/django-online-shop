from django.contrib import admin
from .models import Product, Category

# Register your models here.


@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'quantity', 'price', 'discount', 'final_price')
    list_editable = ('quantity',)
    list_filter = ('category',)
    list_per_page = 10
    prepopulated_fields = {
        'slug': ('title',)
    }

    def category(self, product):
        return ', '.join([item for item in product.category])

    def discount(self, product):
        if product.promotion:
            return f"{(product.promotion.discount) * 100}%"
        return 0

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('promotion')
