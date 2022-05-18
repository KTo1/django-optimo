window.onload = function () {

    let quantity, price, orderitem_num;

    let total_forms = parseInt($('input[name=orderitems-TOTAL_FORMS]').val())

    $('.order_form').on('click', 'input[type=number]', function (){
        orderSummaryUpdate()
    });

    $('.order_form').on('click', 'input[type=text]', function (){
        orderSummaryUpdate()
    });

    function orderSummaryUpdate(){
        let order_total_cost = 0;
        let order_total_quantity = 0;

        for (let i = 0; i < total_forms; i++) {
            quantity = parseInt($('input[name=orderitems-' + i + '-quantity]').val()) || 0;
            price = parseInt($('input[name=orderitems-' + i + '-price]').val()) || 0;
            del = $('input[name=orderitems-' + i + '-DELETE]').val() || 0;
            if (del){ continue;};

            order_total_cost += quantity * price;
            order_total_quantity += quantity;

        };

        $('.order_total_cost').html(order_total_cost.toString() + ',00');
        $('.order_total_quantity').html(order_total_quantity.toString());
    };

    $('.formset_row').formset({
        addText: 'Добавить продукт',
        deleteText: 'Удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem
    });

    function deleteOrderItem(row){
        orderSummaryUpdate()
    }
}
