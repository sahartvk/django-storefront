from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F
from store.models import *


def say_hello(request):
    ordered_product_ids = OrderItem.objects.values_list('product')

    # products = Product.objects.filter(id=F('product__orderitem_product_id'))
    products = OrderItem.objects.values_list('product__id', 'product__title').distinct().order_by('product__title')

    return render(request, 'hello.html', {'products': list(products)})
