from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page, never_cache
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
        link_object = cache.get(key)
        if link_object is None:
            link_object = ProductCategories.objects.filter(is_active=True)
            cache.set(key, link_object)
        return link_object
    else:
        return ProductCategories.objects.filter(is_active=True)


def get_product_cached(pk):
    if settings.LOW_CACHE:
        key = 'link_product'
        link_object = cache.get(key)
        if link_object is None:
            link_object = Products.objects.get(id=pk)
            cache.set(key, link_object)
        return link_object
    else:
        return Products.objects.get(id=pk)


# @method_decorator(cache_page(3600), name='dispatch')
# @never_cache
class ProductsView(ListView, BaseClassContextMixin):
    ''' view for products'''

    model = Products
    template_name = 'mainapp/products.html'
    title = 'GeekShop - Каталог'
    # categories = ProductCategories.objects.filter(is_active=True)
    # categories = get_category_cached()
    paginate_by = 3
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super(ProductsView, self).get_context_data()
        # context['categories'] = get_category_cached()
        context['categories'] = ProductCategories.objects.filter(is_active=True)
        return context

    def paginate_queryset(self, queryset, page_size):
        if self.kwargs.get('category_id'):
            queryset = queryset.filter(category_id=self.kwargs.get('category_id'))

        qs = super(ProductsView, self).paginate_queryset(queryset, page_size)

        return qs


class ProductDetail(DetailView):
    ''' view for product detail '''

    model = Products
    template_name ='mainapp/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data()
        context['Product'] = get_product_cached(self.kwargs.get('pk'))
        return context


def get_price(request, pk):
    ''' price ajax request '''

    product_price = Products.objects.get(id=pk).price
    return JsonResponse({'result': product_price})