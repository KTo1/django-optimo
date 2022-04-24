from django.views.generic import DetailView, TemplateView, ListView
# Create your views here.
from mainapp.mixin import BaseClassContextMixin
from mainapp.models import ProductCategories, Products


class IndexTemplateView(TemplateView, BaseClassContextMixin):
    ''' view for index '''

    template_name = 'mainapp/index.html'
    title = 'GeekShop'


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