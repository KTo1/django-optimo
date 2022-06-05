
from django.urls import path
# from adminapp.views import products

from adminapp.views import (IndexTemplateView, UserListView, UserCreateView, UserUpdateView, UserDeleteView,
                            CategoriesListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
                            ProductListView, ProductCreateView,
                            ProductUpdateView, ProductDeleteView, OrdersList, OrderUpdate, order_next, order_cancel,
                            ActionsListView, ActionCreateView, ActionUpdateView, ActionDeleteView)

app_name = 'adminapp'
urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),

    path('users/', UserListView.as_view(), name='admin_users'),
    path('user-create/', UserCreateView.as_view(), name='admin_user_create'),
    path('user-update/<int:pk>/', UserUpdateView.as_view(), name='admin_user_update'),
    path('user-delete/<int:pk>/', UserDeleteView.as_view(), name='admin_user_delete'),

    path('orders/', OrdersList.as_view(), name='admin_orders'),
    path('order-update/<int:pk>/', OrderUpdate.as_view(), name='admin_order_update'),
    path('order-next/<int:pk>/', order_next, name='admin_order_next'),
    path('order-cancel/<int:pk>/', order_cancel, name='admin_order_cancel'),

    path('categories/', CategoriesListView.as_view(), name='admin_categories'),
    path('category-create/', CategoryCreateView.as_view(), name='admin_category_create'),
    path('category-update/<int:pk>/', CategoryUpdateView.as_view(), name='admin_category_update'),
    path('category-delete/<int:pk>/', CategoryDeleteView.as_view(), name='admin_category_delete'),

    path('products/', ProductListView.as_view(), name='admin_products'),
    path('product-create/', ProductCreateView.as_view(), name='admin_product_create'),
    path('product-update/<int:pk>/', ProductUpdateView.as_view(), name='admin_product_update'),
    path('product-delete/<int:pk>/', ProductDeleteView.as_view(), name='admin_product_delete'),

    path('actions/', ActionsListView.as_view(), name='admin_actions'),
    path('action-create/', ActionCreateView.as_view(), name='admin_action_create'),
    path('action-update/<int:pk>/', ActionUpdateView.as_view(), name='admin_action_update'),
    path('action-delete/<int:pk>/', ActionDeleteView.as_view(), name='admin_action_delete'),
]
