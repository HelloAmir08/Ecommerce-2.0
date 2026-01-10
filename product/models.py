from decimal import Decimal
from django.db.models import Avg
from django.db import models

#Basic model for other models
class BasicModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Category(BasicModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(BasicModel):
    class RatingChoice(models.IntegerChoices):
        ZERO = 0
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    stock = models.BooleanField(default=False)
    rating = models.PositiveIntegerField(choices=RatingChoice.choices, default=RatingChoice.ZERO)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)

    def __str__(self):
        return self.name

    def average_rating(self):
        return self.comments.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

    @property
    def has_discount(self) -> bool:
        return self.discount > 0

    @property
    def discounted_price(self) -> Decimal:
        if not self.has_discount:
            return self.price

        return (
            self.price * (Decimal('100') - Decimal(self.discount)) / Decimal('100')
        ).quantize(Decimal('0.01'))

    @property
    def get_image(self):
        image = self.images.all()[4]
        if image and image.image:
            return image.image.url
        return 'product_images/default.jpg'


class ProductSpecification(BasicModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.key} : {self.value}'

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products_images/', null=True, blank=True)

class Comment(BasicModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()
    rating = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.full_name} - {self.rating} stars'
