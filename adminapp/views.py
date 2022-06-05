# Create your views here.
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView

from actionsapp.models import Action
from adminapp.forms import UserAdminRegisterForm, UserAdminProfileForm, UserAdminCategoryForm, UserAdminProductForm, \
    UserAdminOrderForm, UserAdminActionForm
from authapp.models import User

from mainapp.mixin import BaseClassContextMixin, CustomDispatchMixin, BaseClassDeleteMixin, SuccessMessageMixin
from mainapp.models import ProductCategories, Products
from ordersapp.models import Order, OrderItem


class IndexTemplateView(TemplateView, BaseClassContextMixin, CustomDispatchMixin):
    ''' view for index '''

    template_name = 'adminapp/admin.html'
    title = 'Администраторский раздел - Главная'

# region actions

class ActionsListView(ListView, BaseClassContextMixin, CustomDispatchMixin):
    ''' view for  actions list '''

    model = Action
    template_name = 'adminapp/admin-actions-read.html'
    title = 'Администраторский раздел - акции'


class ActionCreateView(CreateView, SuccessMessageMixin, BaseClassContextMixin, CustomDispatchMixin):
    ''' view for create action '''

    model = Action
    template_name = 'adminapp/admin-action-create.html'
    title = 'Администраторский раздел - Создание акции'
    form_class = UserAdminActionForm
    success_message = "Акция успешно создана."
    success_url = reverse_lazy('adminapp:admin_actions')

    def post(self, request, *args, **kwargs):
        category = ProductCategories.objects.get(pk=request.POST['category'])
        percent = int(request.POST['percent'])
        Action.update_products(category, percent)
        return super(ActionCreateView, self).post(request, *args, **kwargs)


class ActionUpdateView(UpdateView, SuccessMessageMixin, BaseClassContextMixin, CustomDispatchMixin):
    ''' view for update category '''

    model = Action
    template_name = 'adminapp/admin-action-update-delete.html'
    title = 'Администраторский раздел - Редактирование акции'
    form_class = UserAdminActionForm
    success_message = "Акция успешно обновлена."
    success_url = reverse_lazy('adminapp:admin_actions')

    def post(self, request, *args, **kwargs):
        action = self.get_object()
        Action.update_products(action.category, action.percent)
        return super(ActionUpdateView, self).post(request, *args, **kwargs)


class ActionDeleteView(BaseClassDeleteMixin, CustomDispatchMixin):
    ''' view for delete action '''

    model = Action
    template_name = 'adminapp/admin-action-update-delete.html'
    success_url = reverse_lazy('adminapp:admin_actions')

    def post(self, request, *args, **kwargs):
        action = self.get_object()
        Action.update_products(action.category, 0)
        return super(ActionDeleteView, self).post(request, *args, **kwargs)

# endregion

# region users

class UserListView(ListView, BaseClassContextMixin, CustomDispatchMixin):
    ''' view for user list '''

    model = User
    template_name = 'adminapp/admin-users-read.html'
    title = 'Администраторский раздел - Пользователи'
    context_object_name = 'users'


class UserCreateView(CreateView, SuccessMessageMixin, BaseClassContextMixin, CustomDispatchMixin):
    ''' view for create user '''

    model = User
    template_name = 'adminapp/admin-users-create.html'
    title = 'Администраторский раздел - Создание пользователя'
    form_class = UserAdminRegisterForm
    success_message = "Пользователь успешно создан."
    success_url = reverse_lazy('adminapp:admin_users')


class UserUpdateView(UpdateView, SuccessMessageMixin, BaseClassContextMixin, CustomDispatchMixin):
    ''' view for update user '''

    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    title = 'Администраторский раздел - Редактирование пользователя'
    form_class = UserAdminProfileForm
    context_object_name = 'user_select'
    success_message = "Пользователь успешно отредактирован."
    success_url = reverse_lazy('adminapp:admin_users')


class UserDeleteView(BaseClassDeleteMixin, CustomDispatchMixin):
    ''' view for delete user '''

    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    success_url = reverse_lazy('adminapp:admin_users')
    context_object_name = 'user_select'


#endregion

# region orders

class OrdersList(ListView, BaseClassContextMixin, CustomDispatchMixin):
    ''' view for orders list '''

    model = Order
    template_name = 'adminapp/admin-orders-read.html'
    title = 'Администраторский раздел - Заказы'

class OrderUpdate(UpdateView, SuccessMessageMixin, BaseClassContextMixin, CustomDispatchMixin):
    ''' view for update order '''

    model = Order
    template_name = 'adminapp/admin-orders-update-delete.html'
    title = 'Администраторский раздел - Редактирование заказа'
    form_class = UserAdminOrderForm
    success_message = "Заказ успешно отредактирован."
    success_url = reverse_lazy('adminapp:admin_orders')


@login_required
def order_next(request, pk):
    ''' view for change order status to next '''

    order = Order.objects.get(pk=pk)
    if order.can_processed():
        order.status = order.get_next_status(order.status)
        order.save()

    return HttpResponseRedirect(reverse('adminapp:admin_orders'))

@login_required
def order_cancel(request, pk):
    ''' view for change order status to cancel '''

    order = Order.objects.get(pk=pk)
    if order.can_processed():
        order.status = Order.CANCEL
        order.save()

        items = OrderItem.objects.filter(order_id=order.id)
        for item in items:
            product = Products.objects.get(id=item.product_id)
            # product.quantity += item.quantity
            product.quantity = F('quantity') + item.quantity
            product.save()

    return HttpResponseRedirect(reverse('adminapp:admin_orders'))

#endregion

# region categories

class CategoriesListView(ListView, BaseClassContextMixin, CustomDispatchMixin):
    ''' view for user list '''

    model = ProductCategories
    template_name = 'adminapp/admin-categories-read.html'
    title = 'Администраторский раздел - Категории'


class CategoryCreateView(CreateView, SuccessMessageMixin, BaseClassContextMixin, CustomDispatchMixin):
    ''' view for create category '''

    model = ProductCategories
    template_name = 'adminapp/admin-categories-create.html'
    title = 'Администраторский раздел - Создание категории'
    form_class = UserAdminCategoryForm
    success_message = "Категория успешно создана."
    success_url = reverse_lazy('adminapp:admin_categories')


class CategoryUpdateView(UpdateView, SuccessMessageMixin, BaseClassContextMixin, CustomDispatchMixin):
    ''' view for update category '''

    model = ProductCategories
    template_name = 'adminapp/admin-categories-update-delete.html'
    title = 'Администраторский раздел - Редактирование категории'
    form_class = UserAdminCategoryForm
    success_message = "Категория успешно обновлена."
    success_url = reverse_lazy('adminapp:admin_categories')


class CategoryDeleteView(BaseClassDeleteMixin, CustomDispatchMixin):
    ''' view for delete category '''

    model = ProductCategories
    success_url = reverse_lazy('adminapp:admin_categories')

    def update_sub_elements(self, category):
        sub_elements = Products.objects.filter(category=category)
        for element in sub_elements:
            element.is_active = category.is_active
            element.save()

    def post(self, request, *args, **kwargs):
        post = super(CategoryDeleteView, self).post(request, *args, **kwargs)
        self.update_sub_elements(self.get_object())
        return post

#endregion

# region products

class ProductListView(ListView, BaseClassContextMixin, CustomDispatchMixin):
    ''' view for products list '''

    model = Products
    template_name = 'adminapp/admin-products-read.html'
    title = 'Администраторский раздел - Продукты'
    context_object_name = 'products'


class ProductCreateView(CreateView, SuccessMessageMixin, BaseClassContextMixin, CustomDispatchMixin):
    ''' view for create product '''

    model = Products
    template_name = 'adminapp/admin-products-create.html'
    title = 'Администраторский раздел - Создание продукта'
    form_class = UserAdminProductForm
    success_message = "Продукт успешно создан."
    success_url = reverse_lazy('adminapp:admin_products')


class ProductUpdateView(UpdateView, SuccessMessageMixin, BaseClassContextMixin, CustomDispatchMixin):
    ''' view for update product '''

    model = Products
    template_name = 'adminapp/admin-products-update-delete.html'
    title = 'Администраторский раздел - Редактирование продукта'
    form_class = UserAdminProductForm
    context_object_name = 'product_select'
    success_message = "Продукт успешно обновлен."
    success_url = reverse_lazy('adminapp:admin_products')


class ProductDeleteView(BaseClassDeleteMixin, CustomDispatchMixin):
    ''' view for delete product '''

    model = Products
    success_url = reverse_lazy('adminapp:admin_products')
    context_object_name = 'product_select'


#endregion