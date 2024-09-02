from django.http import HttpResponse
from django.shortcuts import render

from pizzas.models import Pizza


# Create your views here.


def index(request):
    return render(request, 'pizzas/index.html')


def pizzas(request):
    pizzas = Pizza.objects.all()
    context = {'pizzas': pizzas}
    return render(request, 'pizzas/pizzas.html', context=context)


def pizza_details(request, pizza_id):
    try:
        pizza = Pizza.objects.get(id=pizza_id)
    except Pizza.DoesNotExist:
        return HttpResponse('Pizza does not exist')
    except Pizza.MultipleObjectsReturned:
        return HttpResponse('找到多条匹配记录！')
    toppings = pizza.topping_set.all()
    context = {'pizza': pizza, 'toppings': toppings}
    return render(request, 'pizzas/pizza.html', context=context)
