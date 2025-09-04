from django.urls import path
from . import views

urlpatterns = [
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),  #url pattern to add product to cart
    path('minus/<int:product_id>/', views.minus_cart, name='minus_cart'),  #url pattern to remove product from cart
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),  #url pattern to remove product from cart
    path('', views.cart, name='cart'),  #url pattern to display cart   
    path('checkout/', views.checkout, name='checkout'),
    #path('checkout/', views.checkout, name='checkout'),  #url pattern to display checkout page
]