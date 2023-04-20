from django.contrib import admin
from .models import Product, Category, Promotion


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('discount', )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_category', 'quantity', 'price', 'discount', 'final_price')
    list_editable = ('quantity',)
    list_filter = ('category',)
    list_per_page = 10
    prepopulated_fields = {
        'slug': ('title',)
    }

    def get_category(self, product):
        return ', '.join([item.title for item in product.category.all()])

    def discount(self, product):
        if product.promotion:
            return f"{int((product.promotion.discount) * 100)}%"
        return 0

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('promotion')
