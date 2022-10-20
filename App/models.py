from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User,AbstractUser


class Address(models.Model):
    first_name = models.CharField(max_length=50,blank=True,null=True)
    last_name = models.CharField(max_length=50,blank=True,null=True)
    username = models.CharField(max_length=50,blank=True,null=True)
    Address= models.CharField(max_length=250 ,blank=True,null=True)
    optional_address = models.CharField(max_length=150,blank=True,null=True)
    city= models.CharField(max_length=150,blank=True,null=True)
    state= models.CharField(max_length=50,blank=True,null=True)
    zip= models.CharField(max_length=50,blank=True,null=True)
    country= models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.Address




class MyUser(AbstractUser):
    mobile_no = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10,blank=True,null=True)
    address = models.ForeignKey(Address,on_delete=models.DO_NOTHING,blank=True,null=True)


# Create your models here.
class ProductItem(models.Model):
    product = models.CharField(max_length=30,blank=False)

    def __str__(self):
        return self.product
    

class Product_details(models.Model):
    def namFile(instance, filename):
        return '/'.join(['Prodcut_images',str(instance.product_title), filename])
        
    product_name = models.ForeignKey(ProductItem, on_delete=models.DO_NOTHING)
    
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
    user = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING,null=True)
    product=models.ForeignKey(Product_details,on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    def __str__(self):
        return 'User'+" = "+self.user.username + ', Quantity = ' + str(self.quantity) + ', product name' + self.product.product_title
    
class OrderList(models.Model):
    product = models.ForeignKey(Product_details,on_delete=models.DO_NOTHING,blank=True, null=True)
    quantity = models.IntegerField(null=True)
    user = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING,null=True)
    def __str__(self):
        return 'Product name'+" = "+self.product.product_title + ', Quantity = ' + str(self.quantity) + ', User = ' + self.user.username

class Orders(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING)
    product = models.ManyToManyField(OrderList)
    delivery_address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    payment_method = models.CharField(max_length=100)
    orderId = models.CharField(max_length=35,null=True,blank=True)





    
    