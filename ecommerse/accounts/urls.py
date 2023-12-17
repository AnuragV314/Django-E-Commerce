from django.urls import path
from . import views
# from products.views import 

urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('activate/<email_token>/', views.activate_email, name="activate_email"),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<uid>/', views.add_to_cart, name='add_to_cart'),
    path('remove-cart/<cart_item_uid>', views.remove_cart, name="remove_cart"),
    path('', views.continue_shopping, name='continue_shopping'),

]
