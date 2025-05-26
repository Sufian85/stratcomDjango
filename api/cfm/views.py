from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . serialiser import *
from . models import *
from django.db import transaction
from django.db.models import Q

# Create your views here.
@api_view(["GET"])
def home_view(request):
    msg = {
        "msg":"Welcome to our api endpoints"
    }
    return Response(msg, status=status.HTTP_200_OK)

@api_view(["GET", "POST"])
def products_view(request):
    if request.method == "GET":
        search = request.GET.get("search")
        min_price = request.GET.get("min-price")
        max_price = request.GET.get("max-price")
        all_prod = Product.objects.all()
        if search:
            all_prod = all_prod.filter(
                Q(name__icontains = search) |
                Q(description__icontains = search))
        if min_price and max_price:
            all_prod = all_prod.filter(
                price__range = [min_price, max_price])
        serializer = productSerializer(all_prod, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        data = request.data
        serializer = productSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def product_detail_view(request, **kwargs):
    id = kwargs['id']
    try:
        product = Product.objects.get(pk = id)
    except Product.DoesNotExist as e:
        return Response(
            {"error":f"{e}"}, status=status.HTTP_404_NOT_FOUND
        )
    if request.method == "GET":
        serializer = productSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        data = request.data
        serializer = productSerializer(product, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        product.delete()
        return Response({"msg":"item deleted"}, status=status.HTTP_204_NO_CONTENT)
    
@api_view(["POST"])
def create_order(request):
    def order_content(order_info, item_info):
        with transaction.atomic():
            #order = Order.objects.create(**order_info)
            order = Order.objects.create(
                owner = User.objects.get(id=order_info['owner'])
            )

            for item in item_info:
                # check for available quantity 
                product = Product.objects.get(id = item['product'])
                if product.qty >= int(item['qty']):
                    #OrderItems.objects.create(**item)
                    OrderItems.objects.create(
                        product = Product.objects.get(id=item['product']),
                        order = order,
                        qty = item['qty'],
                        amount = item['amount']
                    )
                    # reduce produce stock
                    product.qty = int(product.qty) - int(item['qty'])
                    product.save()
        return order
    
    data = request.data
    print(data)
    created_order = order_content(data['order_info'], data['item_info'])
    serializer = OrderSerializer(created_order)
    msg = {
        "msg":"order created successfully",
        "order": serializer.data
    }
    return Response(msg, status=status.HTTP_201_CREATED)

@api_view(["GET"])
def get_order_info(request, orderId):
    try:
        order = Order.objects.prefetch_related("items").get(pk = orderId)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Order.DoesNotExist as e:
        return Response({"error":f"{e}"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
def get_all_orders(request):
    try:
        orders = Order.objects.prefetch_related("items").all()
        serializer = OrderSerializer(orders, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Order.DoesNotExist as e:
        return Response({"error":f"{e}"}, status=status.HTTP_404_NOT_FOUND)
    

# pesapal - payment
"""
developer pesapal
create an access token 
ipn 
request to pay 
check payment status
completed
""" 