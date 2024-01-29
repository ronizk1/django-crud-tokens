from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None) 
    desc = models.CharField(max_length=50,null=True,blank=True)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)  
    createdTime=models.DateTimeField(auto_now_add=True)
    fields =['desc','price']
 
    def __str__(self):
           return self.desc