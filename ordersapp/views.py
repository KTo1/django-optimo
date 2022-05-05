from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from basketapp.models import Basket
from mainapp.mixin import BaseClassContextMixin, UserDispatchMixin, SuccessMessageMixin
from ordersapp.forms import OrderItemsForm
from ordersapp.models import Order, OrderItem


class OrderList(ListView, BaseClassContextMixin):
    ''' view for orders list'''
    # если название класса + базовый класс соответствует названию темплейта, то имя темплейта можно не указывать
    # order + list = order_list.html
    model = Order
    title = 'GeekShop - Заказы'


class OrderCreate(CreateView, BaseClassContextMixin):
    ''' view for order create '''

    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')
    title = 'GeekShop - Новый заказ'

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data()

        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=1)
        if self.request.POST:
            form_set = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items:
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=basket_items.count())
                form_set = OrderFormSet()

                for num, form in enumerate(form_set.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
                # basket_items.delete()
            else:
                form_set = OrderFormSet()

        context['orderitems'] = form_set

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']
        
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()

            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
                Basket.objects.filter(user=self.request.user).delete()

            if self.object.get_total_cost() == 0:
                self.object.delete()
                
            return super(OrderCreate, self).form_valid(form)    
            
        
class OrderUpdate(UpdateView, BaseClassContextMixin):
    ''' view for order update '''

    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')
    title = 'GeekShop - Новый заказ'

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data()

        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=1)
        if self.request.POST:
            form_set = OrderFormSet(self.request.POST, instance=self.object)
        else:
            form_set = OrderFormSet(instance=self.object)
            for num, form in enumerate(form_set.forms):
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

        context['orderitems'] = form_set

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            if self.object.get_total_cost() == 0:
                self.object.delete()

            return super(OrderUpdate, self).form_valid(form)


class OrderRead(DetailView):
    ''' view for order detail '''

    model = Order
    title = 'GeekShop - Заказ'


class OrderDelete(DeleteView):
    ''' view for order delete '''

    model = Order
    success_url = reverse_lazy('ordersapp:list')
    title = 'GeekShop - Удаление заказа'


def forming_complete(requets, pk):
    ''' view for order change status '''

    order = Order.objects.get(pk=pk)
    order.status = Order.SEND_TO_PROCESSED
    order.save()

    return HttpResponseRedirect(reverse('ordersapp:list'))