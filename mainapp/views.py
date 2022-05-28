from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, TemplateView, ListView

# Create your views here.
from mainapp.mixin import BaseClassContextMixin
from mainapp.models import ProductCategories, Products


class IndexTemplateView(TemplateView, BaseClassContextMixin):
    ''' view for index '''

    template_name = 'mainapp/index.html'
    title = 'GeekShop'


@cache_page(3600)
class ProductsView(ListView, BaseClassContextMixin):
    ''' view for products'''

    model = Products
    template_name = 'mainapp/products.html'
    title = 'GeekShop - Каталог'
    categories = ProductCategories.objects.filter(is_active=True)
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