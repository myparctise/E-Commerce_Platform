
from http.client import HTTPResponse
from itertools import product
from typing import Optional
from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import Product_details,ProductItem,AddToCart,MyUser,OrderList,Address,Orders
from .serializer import Product_Serializer,show_product_serializer
from django.http import Http404
from django.db.models import Sum,F,Q,ExpressionWrapper
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator
from .filters import SearchingFilter
import razorpay
from django.conf import settings
from django.http import JsonResponse






class UserProduct(viewsets.ViewSet):

    def list(self, request):
        database_data = Product_details.objects.all()
        serializer = show_product_serializer(database_data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


    def create(self, request):
        data = request.data
        print(data)
        raw = data['product_name']
        print(raw,"--------------------------")
        response = ProductItem.objects.filter(product=raw).values('id')
        product_instance = list(response)
        data['product_name'] = product_instance[0]['id']
        print(data)
        serializer = Product_Serializer(data = data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        instance = Product_details.objects.get(pk = pk)
        serializer = show_product_serializer(instance)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        instance = Product_details.objects.get(pk = pk)
        data = request.data
        print(data)
        raw = data['product_name']
        print(raw,"--------------------------")
        response = ProductItem.objects.filter(product=raw).values('id')
        product_instance = list(response)
        data['product_name'] = product_instance[0]['id']
        print(data)
        serializer = Product_Serializer(instance,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        instance = Product_details.objects.get(pk = pk)
        data = request.data
        print(data)
        raw = data['product_name']
        print(raw,"--------------------------")
        response = ProductItem.objects.filter(product=raw).values('id')
        product_instance = list(response)
        data['product_name'] = product_instance[0]['id']
        print(data)
        serializer = Product_Serializer(instance,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        instance = Product_details.objects.get(pk = pk)
        instance.delete()
        return Response("Data is deleted")

# Template Part start


def home_Page(request):
    if request.method == 'GET':
        data = Product_details.objects.all()
        # print(request.user.id)
        return render(request,'index.html',{'data':data})

def Products(request,slug=None):
    if slug:
        data = Product_details.objects.get(slug = slug)
        product_data = Product_details.objects.filter(product_name_id=data.product_name.id)[0:4]
        print(request.user.id,"----------")
        id = request.user.id
        return render(request,'single-product.html',{'d':data,"database_data":product_data,"user_id":id})

    return Http404("Page not found")



def Add_to_cart(request):
    if request.method == "POST":
        try:
            ab = AddToCart.objects.get(product_id = request.POST['pid'],user_id=request.POST['ui'])
            ab.quantity += int(request.POST['quantity'])
            ab.save()

        except:
            ab = AddToCart(user_id=request.POST['ui'],product_id=request.POST['pid'],quantity=request.POST['quantity'])
            ab.save()
    product = AddToCart.objects.filter(user_id = request.user.id).order_by('-id')
    # pro_id = product.values('product_id')
    # print(pro_id)
    # pro_price = Product_details.objects.filter(id__in=pro_id).aggregate(Sum('product_price'))

    # print(pro_price)
    #tot_price = pro_price['product_price__sum']
    #print(tot_price)
    
    
    return render(request,"cart.html",{"cart_product":product})

def UpdateQuantity(request):
    if request.method == "POST":
        oobj = request.POST
        print(oobj)
        print(oobj['id'])
        instance = AddToCart.objects.get(id = oobj['id'])
        instance.quantity = oobj["quantity"]
        instance.save()
        return JsonResponse({"response":"success"})


def RemoveCart(request,pk):
    ab = AddToCart.objects.get(id=pk)
    ab.delete()
    return redirect('/mycart/')

#Authentication System

def RegisterUser(request):
    if request.method == "GET":
        return render(request,'register.html')
    elif request.method == "POST":
        first_name = request.POST.get('firstname')
        last_name = request.POST['lastname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']
        gender = request.POST['radiogroup1']
        mobile_number = request.POST['mobile_number']

        if password == confirm_password:
            if MyUser.objects.filter(username = username).exists():
                messages.info(request,"Username is already exists")
                return redirect('register')
            elif MyUser.objects.filter(email=email).exists():
                messages.info(request,"Email is already exists")
                return redirect('register')
            elif MyUser.objects.filter(mobile_no = mobile_number).exists():
                messages.info(request,"mobile_number is already exists")
                return redirect('register')
            else:
                data = MyUser.objects.create_user(first_name = first_name, last_name = last_name,
                                                email = email, username = username, password = password,
                                                gender = gender, mobile_no = mobile_number)
                data.save()
                return redirect('login')
        else:
            messages.info(request,"Password is not correct")
            return redirect('register')

# This fucntion for login
def login_user(request):
    if request.method =="GET":
        return render(request,"login.html")
    elif request.method == "POST":
        try:
            data = request.POST['username']
            password = request.POST['password']
        except Exception as e :
            print(e)
        

        try: 
            user = MyUser.objects.get(username=data)
        except:
            try:
                user = MyUser.objects.get(email=data)
            except:
                try:
                    user = MyUser.objects.get(mobile_no=data)
                except:
                    messages.info(request,"Invalid info")
                    return redirect('login')


        if user is not None:
                if user.check_password(password):
                    login(request,user)
                    return redirect('home')
                else:
                    messages.info(request,"Invalid info")
                    return redirect('login')
        else:
            messages.info(request,"Invalid info")
            return redirect('login')
        
                
            
def Logout(request):
    logout(request)
    return redirect('login')

def All_products_data(request):
    if request.method == "GET":
        data = Product_details.objects.all()
        try:
            searching = SearchingFilter(request.GET,queryset=data)
        except:
            pass

        paginator = Paginator(searching.qs, 2) # Show 25 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        

        return render(request,"products.html",{"data":page_obj,"search":searching})

def Checkout_page(request):
    instancee = AddToCart.objects.filter(user_id = request.user.id).annotate(totprice=F("product__product_price")* F("quantity"))
    if request.method == "GET":
        print(instancee.values())
        tot_price = instancee.aggregate(Sum('totprice'))
        print(tot_price)

        client = razorpay.Client(auth=(settings.KEY,settings.SECRET) )
        payment =  client.order.create({'amount':tot_price['totprice__sum']*100, 'currency':'INR', "payment_capture":1 })
        print(payment,"----------Here ---------1")
        return render(request,"checkout.html",{"data":instancee,'tot_price':tot_price['totprice__sum'],"payment":payment})

    elif request.method == "POST":
        print(instancee.values())

        tot_price = instancee.aggregate(Sum('totprice'))
        print(tot_price)

        client = razorpay.Client(auth=(settings.KEY,settings.SECRET) )
        payment =  client.order.create({'amount':tot_price['totprice__sum']*100, 'currency':'INR', "payment_capture":1 })
        print(payment,"----------Here ---------2")

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username =  request.POST['username']
        email =  request.POST['email']
        address =  request.POST['address']
        address2 =  request.POST['address2']
        country = request.POST['country']
        state =  request.POST['state']
        zip = request.POST['zip']
        paymentMethod =  request.POST['paymentMethod']
        data = Address(first_name = first_name,last_name= last_name,email=email,username=username,Address=address,optional_address =address2,
                                        country=country,state=state,zip=zip)
        print('inside')
        data.save()



        try:
            checkbox = request.POST['check']

            abcd = MyUser.objects.get(id=request.user.id)
            abcd.address_id = data.id
            abcd.save()

        except:
            print('error')
        cart_ides = list(instancee.values('id'))
        pi = list(instancee.values('product_id'))
        quantity_values = list(instancee.values("quantity"))
        print(quantity_values)
        ab = []
        for i in range(len(pi)):
            # print("prduct_id:-",pi[i]['product_id'],"quantity:-",quantity_values[i]["quantity"])
            obj = OrderList.objects.create(product_id = pi[i]['product_id'],quantity = quantity_values[i]['quantity'],user_id = request.user.id)
            obj.save()
            ab.append(obj.id)

            instance = AddToCart.objects.get(id = cart_ides[i]["id"])
            instance.delete()  

            print(paymentMethod,"=========+++++++")
            

            #COD
        orderObj = Orders.objects.create(user_id = request.user.id,delivery_address_id=data.id,
                    payment_method = paymentMethod)
        for i in ab:
            obj =OrderList.objects.get(id = i)
            orderObj.product.add(i)

        return render(request,'cod.html')

