from basketapp.models import Basket


def basket(request):
    baskets = []
    if request.user.is_authenticated:
        baskets = Basket.objects.filter(user=request.user).select_related()
        basket_total_sum = 0
        basket_total_quantity = 0
        for basket in baskets:
            basket_total_sum += basket.quantity * basket.product.price
            basket_total_quantity += basket.quantity

    return {'baskets': baskets, 'basket_total_sum': basket_total_sum, 'basket_total_quantity': basket_total_quantity}