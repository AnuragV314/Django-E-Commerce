from django.db import models
from base.models import BaseModel

from django.utils.text import slugify
# Create your models here.


class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_image = models.ImageField(upload_to="category")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name


class ColorVarient(BaseModel):
    color_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.color_name


class SizeVarient(BaseModel):
    size_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.size_name


class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    catogory = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products")
    price = models.IntegerField()
    product_desc = models.TextField()

    color_varient = models.ManyToManyField(ColorVarient, blank=True)
    size_varient = models.ManyToManyField(SizeVarient, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name

    def get_product_price_by_size(self, size):
        size_varient = SizeVarient.objects.get(size_name=size)
        return self.price + size_varient.price


class ProductImage(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product')




class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)













