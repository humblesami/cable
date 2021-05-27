import asyncio

from django.db import connection

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from noman.methods import now_str
from noman.models import Area, Subscription, SaleObject


def get_subscription_charges(request):
    subscription_id = request.GET.get('subscription_id')
    res = ''
    if subscription_id:
        subscription_id = int(subscription_id)
        obj = Subscription.objects.get(pk=subscription_id)
        res = obj.installment
    res = HttpResponse(res)
    return res


def get_due_amount(request):
    sale_object_id = request.GET.get('sale_object_id')
    res = ''
    if sale_object_id:
        sale_object_id = int(sale_object_id)
        obj = SaleObject.objects.get(pk=sale_object_id)
        res = obj.installment
    res = HttpResponse(res)
    return res


def index(request):
    return HttpResponse('Index Page')


def million_areas(request):
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # result = loop.run_until_complete(fun2("django"))
    result = ''
    print(now_str())
    fun1()
    print(now_str())
    result = str(result)
    return HttpResponse('done--' + str(result))


async def fun2(hi):
    res = await fun3()
    return res


async def fun3():
    print(144)
    return 344


def fun1(obj_method=None):
    million = 500000
    cnt = len(Area.full.all())
    ar_obj = []
    i = cnt
    while i <= million:
        i_str = str(i)
        i_str = 'million-' + i_str
        ar_obj.append(Area(name=i_str))
        i += 1

    if len(ar_obj):
        Area.full.bulk_create(ar_obj)

        cnt = len(Area.full.all())
        query = "insert into noman_area (name) values(%s)"
        j = cnt + 1
        ar_values = ['million-' + str(cnt)]
        million += million
        while j <= million:
            j_str = 'million-' + str(j)
            ar_values.append(j_str)
            query += ",(%s)"
            j += 1
        if len(ar_values):
            with connection.cursor() as cursor:
                cursor.execute(query, ar_values)
    return 'done'
