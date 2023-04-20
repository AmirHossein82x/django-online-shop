from django.db import models

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Promotion(models.Model):
    discount = models.DecimalField(max_digits=3, decimal_places=2)

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

    def final_price(self):
        if self.promotion:
            return self.price * (1 - self.promotion.discount)
        return self.price

