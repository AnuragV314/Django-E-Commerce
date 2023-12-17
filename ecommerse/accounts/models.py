from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel

from django.db.models.signals import post_save
from django.dispatch import receiver 
import uuid
from base.emails import send_account_activation_email
from products.models import Coupon, Product, ColorVarient, SizeVarient
from decimal import Decimal

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_email_verified = models.BooleanField(default=True)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile')


    def get_cart_count(self):
        return CartItems.objects.filter(cart__is_paid=False, cart__user=self.user).count()





class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    is_paid = models.BooleanField(default = False)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null = True, blank=True)

    

    def calculate_totals(self):
        total_price = sum(cart_item.get_product_price() for cart_item in self.cart_items.all())
        discount = Decimal('0.00')  # Default discount
        
        if self.coupon:
            # If a coupon is applied, use the coupon's discount value
            if total_price > self.coupon.minimum_amount:
                discount = Decimal(str(self.coupon.discount_price))
        
        final_total = max(Decimal('0.00'), total_price - discount)

        return {
            'total_price': total_price,
            'discount': discount,
            'final_total': final_total,
        }


class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name = 'cart_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)

    color_varient = models.ManyToManyField(ColorVarient)
    size_varient = models.ManyToManyField(SizeVarient)

   
    def get_product_price(self):
        price = 0  

        if self.product:
            price += self.product.price 

        if self.color_varient.exists():
            color_varient_price = sum(variant.price for variant in self.color_varient.all() if variant.price is not None)
            price += color_varient_price

        if self.size_varient.exists():
            size_varient_price = sum(variant.price for variant in self.size_varient.all() if variant.price is not None)
            price += size_varient_price

        return price







# signal (User)
@receiver(post_save , sender = User)
def  send_email_token(sender , instance , created , **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user = instance , email_token = email_token)
            email = instance.email
            send_account_activation_email(email , email_token)

    except Exception as e:
        print(e)
        



