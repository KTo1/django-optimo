from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, TemplateView, ListView

# Create your views here.
from mainapp.mixin import BaseClassContextMixin
from mainapp.models import ProductCategories, Products


class IndexTemplateView(TemplateView, BaseClassContextMixin):
    ''' view for index '''

    template_name = 'mainapp/index.html'
    title = 'GeekShop'


def get_category_cached():
    if settings.LOW_CACHE:
        key = 'link_category'
        link_category = cache.get(key)
        if link_category is None:
            link_category = ProductCategories.objects.filter(is_active=True)
            cache.set(key, link_category)
        return link_category
    else:
        return ProductCategories.objects.filter(is_active=True)


# @method_decorator(cache_page(3600), name='dispatch')
class ProductsView(ListView, BaseClassContextMixin):
    ''' view for products'''

    model = Products
    template_name = 'mainapp/products.html'
    title = 'GeekShop - Каталог'
    # categories = ProductCategories.objects.filter(is_active=True)
    categories = get_category_cached()
    paginate_by = 3
    context_object_name = 'products'

    def paginate_queryset(self, queryset, page_size):
        if self.kwargs.get('category_id'):
            queryset = queryset.filter(category_id=self.kwargs.get('category_id'))

        qs = super(ProductsView, self).paginate_queryset(queryset, page_size)

        return qs


class ProductDetail(DetailView):
    model = Products
    template_name ='mainapp/detail.html'


def get_price(request, pk):
    product_price = Products.objects.get(id=pk).price
    return JsonResponse({'result': product_price})