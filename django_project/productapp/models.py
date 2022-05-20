from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Product(models.Model):
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('productapp:products')

    seller_name = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    name = models.CharField(max_length = 100)
    price = models.IntegerField()
    desc = models.CharField(max_length = 200)
    image = models.ImageField(blank=True,upload_to='images')
    
class CartItem(models.Model):
    def __str__(self):
        return "{}:{}".format(self.product.name, self.id)

    def update_quantity(self, quantity):
        self.quantity = self.quantity + quantity
        self.save()

    def total_cost(self):
        return self.quantity * self.price

    cart_id = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)



class Order(models.Model):
    def __str__(self):
        return "{}:{}".format(self.id, self.email)

    def total_cost(self):
        return sum([ li.cost() for li in self.lineitem_set.all() ] )

    name = models.CharField(max_length=191)
    email = models.EmailField()
    postal_code = models.IntegerField()
    address = models.CharField(max_length=191)
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)


class LineItem(models.Model):
    def __str__(self):
        return "{}:{}".format(self.product.name, self.id)

    def cost(self):
        return self.price * self.quantity
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

class Contact(models.Model):
    def __str__(self):
       return str(self.name)
   
    name = models.CharField(max_length=50,null = True, blank = True)
    email = models.EmailField(null = True, blank = True)
    phone = models.IntegerField(null = True, blank = True)
    desc = models.CharField(max_length=191,null = True, blank = True)