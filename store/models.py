from django.db import models

# Create your models here.


class ProductManager(models.Manager):
    def available(self):
        return self.filter(quantity__gt=0)


class Category(models.Model):
    title = models.CharField(max_length=255)
    date_time_created = models.DateTimeField(auto_now_add=True)
    date_time_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Promotion(models.Model):
    discount = models.DecimalField(max_digits=3, decimal_places=2)
    date_time_created = models.DateTimeField(auto_now_add=True)
    date_time_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.discount)


class Product(models.Model):
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, null=True, blank=True, related_name='products')
    image = models.ImageField(upload_to='product', null=True)
    date_time_created = models.DateTimeField(auto_now_add=True)
    date_time_modified = models.DateTimeField(auto_now=True)
    objects = ProductManager()

    def final_price(self):
        if self.promotion:
            return int(self.price * (1 - self.promotion.discount))
        return self.price

