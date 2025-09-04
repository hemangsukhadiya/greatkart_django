from django.db import models
from store.models import Product
# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)    

    def __str__(self): #this is a magic method that returns a string representation of the object
        return self.cart_id #this will return the cart_id when we call the object of Cart model
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) #foreign key to Product model in store app
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE) #foreign key to Cart model
    quantity =  models.IntegerField()
    isactive = models.BooleanField(default=True)

    def total(self):
        return self.product.price * self.quantity  #this will return the total price of the product in the cart based on the quantity

    def __str__(self):
        return self.product.product_name  #this will return the product name when we call the object of CartItem model
        