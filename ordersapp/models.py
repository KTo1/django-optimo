from django.db import models

from authapp.models import User
from mainapp.models import Products


class Order(models.Model):
    ''' model for orders '''

    FORMING = 'FM'
    SEND_TO_PROCESSED = 'STP'
    PAID = 'PD'
    PROCESSED = 'PRD'
    READY = 'RDY'
    CANCEL = 'CNL'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SEND_TO_PROCESSED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCESSED, 'сборка'),
        (READY, 'готов'),
        (CANCEL, 'отменен'),
    )

    STATUS_ORDER = {
        FORMING: SEND_TO_PROCESSED,
        SEND_TO_PROCESSED: PAID,
        PAID: PROCESSED,
        PROCESSED: READY,
        READY: READY
    }

    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='создан', auto_now=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now_add=True)
    paid = models.DateTimeField(verbose_name='оплачен', null=True, blank=True)
    status = models.CharField(verbose_name='статус', choices=ORDER_STATUS_CHOICES, max_length=3, default=FORMING)
    is_active = models.BooleanField(verbose_name='активен', default=True)

    def __str__(self):
        return f'Текущий заказ {self.pk}'

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x:x.get_product_cost(), items)))

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum([x.quantity for x in items])

    def get_items(self):
        pass

    def can_processed(self):
        return self.status != self.READY and self.status != self.CANCEL

    def get_next_status(self, status):
        return self.STATUS_ORDER[status]

    def delete(self, using=None, keep_parents=False):
        items = self.orderitems.select_related()
        for item in items:
            item.product.quantity += item.quantity
            item.save()

        self.is_active = False
        self.save()


class OrderItem(models.Model):
    ''' model for order items '''

    order = models.ForeignKey(Order, verbose_name='заказ', related_name='orderitems', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, verbose_name='товар', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity

