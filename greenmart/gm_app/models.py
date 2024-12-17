from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    Category_name=models.TextField()
    def __str__(self):
        return self.Category_name
class Product(models.Model):
    pid=models.TextField()
    name=models.TextField()
    dis=models.TextField()
    offer_price=models.IntegerField()
    price=models.IntegerField()
    stock=models.IntegerField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE) 
    # vegitables=models.TextField(null=True, blank=True)
    # fruits=models.TextField(null=True, blank=True)
    img=models.FileField()
    

    
class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    qty=models.IntegerField()