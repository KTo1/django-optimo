from django.conf import settings
from django.core.cache import cache

from basketapp.models import Basket


def get_baskets_cached(user):
    if settings.LOW_CACHE:
        key = 'link_basket'
        link_object = cache.get(key)
        if link_object is None:
            link_object = Basket.objects.filter(user=user).select_related()
            cache.set(key, link_object)
        return link_object
    else:
        return Basket.objects.filter(user=user).select_related()


def basket(request):
    baskets = []
    basket_total_sum = 0
    basket_total_quantity = 0

    if request.user.is_authenticated:
        baskets = Basket.objects.filter(user=request.user).select_related()
        # baskets = get_baskets_cached(user=request.user)
        for basket in baskets:
            basket_total_sum += basket.quantity * basket.product.price
            basket_total_quantity += basket.quantity

    return {'baskets': baskets, 'basket_total_sum': basket_total_sum, 'basket_total_quantity': basket_total_quantity}