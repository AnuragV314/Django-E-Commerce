from django.contrib import admin

# Register your models here.
from .models import Category, Product, ProductImage, ColorVarient, SizeVarient, Coupon

admin.site.register(Category)
admin.site.register(Coupon)

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price']
    inlines = [ProductImageAdmin]


@admin.register(ColorVarient)
class ColorVarientAdmin(admin.ModelAdmin):
    list_display = ['color_name', 'price']
    model = ColorVarient


@admin.register(SizeVarient)
class SizeVarient(admin.ModelAdmin):
    list_display = ['size_name', 'price']
    model = SizeVarient


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
