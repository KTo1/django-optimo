from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string

from basketapp.models import Basket
from mainapp.models import Products

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required
def basket_add(request, product_id):
    ''' view for user basket add'''

    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    product = Products.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=user, product=product)

    if baskets:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    else:
        Basket.objects.create(user=user, product=product, quantity=1)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_remove(request, basket_id):
    ''' view for user basket remove'''

    Basket.objects.get(id=basket_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_edit(request, basket_id, quantity):
    ''' view for user edit'''

    if is_ajax(request):
        basket = Basket.objects.get(id=basket_id)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()

        baskets = Basket.objects.filter(user=request.user)
        context = {'baskets': baskets}

        result = render_to_string('basketapp/basket.html', context)

        return JsonResponse({'result': result})
