from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User,AbstractUser


class MyUser(AbstractUser):
    mobile_no = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10,blank=True,null=True)


# Create your models here.
class ProductItem(models.Model):
    product = models.CharField(max_length=30,blank=False)

    def __str__(self):
        return self.product
    

class Product_details(models.Model):
    def namFile(instance, filename):
        return '/'.join(['Prodcut_images',str(instance.product_title), filename])
        
    product_name = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    
    product_image = models.ImageField(upload_to=namFile,blank=False,null=True)
    product_img1 = models.ImageField(upload_to=namFile,blank=True,null=True)
    product_img2 = models.ImageField(upload_to=namFile,blank=True,null=True)
    product_img3 = models.ImageField(upload_to=namFile,blank=True,null=True)

    product_title = models.CharField(max_length=300,blank=False)
    slug = AutoSlugField(populate_from='product_title',unique=True,null=True)
    short_description = models.CharField(max_length=500,blank=True)
    long_description = models.TextField(blank=False)
    stock = models.IntegerField(blank=True,null=True)
    product_price = models.IntegerField(blank=False)
    on_sale = models.BooleanField(default=False,blank=True, null=True)
    sale_price = models.CharField(max_length=20,blank=True)

    def __str__(self):
        return self.product_title 

    


class AddToCart(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product_details,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    def __str__(self):
        return self.user.username + ' ' + str(self.quantity) + ' ' + self.product.product_title
    
