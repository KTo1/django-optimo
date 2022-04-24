# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView

from adminapp.forms import UserAdminRegisterForm, UserAdminProfileForm, UserAdminCategoryForm, UserAdminProductForm
from authapp.models import User

from mainapp.mixin import BaseClassContextMixin, CustomDispatchMixin, BaseClassDeleteMixin, SuccessMessageMixin
from mainapp.models import ProductCategories, Products


class IndexTemplateView(TemplateView, BaseClassContextMixin, CustomDispatchMixin):
    ''' view for index '''

    template_name = 'adminapp/admin.html'
    title = 'Администраторский раздел - Главная'

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

# region categories

class CategoriesListView(ListView, BaseClassContextMixin, CustomDispatchMixin):
    ''' view for user list '''

    model = ProductCategories
    template_name = 'adminapp/admin-categories-read.html'
    title = 'Администраторский раздел - Категории'
    context_object_name = 'categories'


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
    context_object_name = 'category_select'
    success_message = "Категория успешно обновлена."
    success_url = reverse_lazy('adminapp:admin_categories')


class CategoryDeleteView(BaseClassDeleteMixin, CustomDispatchMixin):
    ''' view for delete category '''

    model = ProductCategories
    success_url = reverse_lazy('adminapp:admin_categories')
    context_object_name = 'category_select'

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