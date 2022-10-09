from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import Product_details,ProductItem
from .serializer import Product_Serializer,show_product_serializer






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

# def start_func(request):
#     if request.method == "GET":
#         return redirect('home')

def home_Page(request):
    if request.method == 'GET':
        data = Product_details.objects.all()
        return render(request,'index.html',{'data':data})

def Products(request):
    return render(request,'single-product.html')