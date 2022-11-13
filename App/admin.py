from django.contrib import admin
from .models import ProductItem,Product_details,AddToCart,Address,Orders,OrderList
from .models import MyUser
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(AddToCart)

@admin.register(ProductItem)
class ProductItem_Admin(admin.ModelAdmin):
    list_display = ['product']

@admin.register(Product_details)
class Product_Admin(admin.ModelAdmin):
    list_display = ['product_name','product_title','slug','product_price','on_sale','sale_price']
    search_fields = ['product_title__contains']


# -------------------- User admin Customisation ---------------------
class CartInline(admin.TabularInline):
    model = AddToCart

class OrderInline(admin.TabularInline):
    model = OrderList

class UserAdmin(UserAdmin):
    model = MyUser
    list_display = ['username','gender','mobile_no','address','is_staff','is_superuser']
    list_filter = ('username','is_staff','is_active','is_superuser')
    fieldsets = (
        ("User Credentials", {
            "fields": (
                'username','password','gender','address','mobile_no'
            ),
        }),
        
        ("User Permissions",{'fields':('is_staff',('is_active','is_superuser'))}),
        ("Important Dates",{"fields":('last_login','date_joined')}),
        ("Advanced options",{
            "classes":("collapse",),
            'fields':('groups','user_permissions')
        })

    )
    inlines = [
        CartInline,OrderInline
    ]
    add_fieldsets = (
        (
            None,{
                'classes':('wide'),
                'fields':('username','password1','password2','is_staff',('is_active','is_superuser'))
            }
        ),
    )

    inlines = [
        CartInline,OrderInline
    ]
    



# admin.site.unregister(MyUser)
admin.site.register(MyUser,UserAdmin)
# -------------------- User admin Customisation end ---------------------


# admin.site.register(Address)
@admin.register(Address)
class Addres(admin.ModelAdmin):
    list_display = ['Address','city','state','zip','country']

@admin.register(Orders)
class Orders_Admin(admin.ModelAdmin):
    list_display = ['user','delivery_address','payment_method']


@admin.register(OrderList)
class OrderListAdmin(admin.ModelAdmin):
    list_display = ['user','product','quantity']

