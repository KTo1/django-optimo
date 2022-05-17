window.onload = function () {

    let quantity, price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;

    let quantity_array = [];
    let price_array = [];

    let total_forms = parseInt($('input[name=orderitems-TOTAL_FORMS]').val())
    let order_total_cost = parseInt($('.order_total_cost').text().replace(',', '.')) || 0;
    let order_total_quantity = parseInt($('.order_total_quantity').text().replace(',', '.')) || 0;


    for (let i = 0; i < total_forms; i++) {
        quantity = parseInt($('input[name=orderitems-' + i + '-quantity]').val()) || 0;
        price = parseInt($('input[name=orderitems-' + i + '-price]').val()) || 0;

        quantity_array[i] = quantity
        price_array[i] = price
    }

    $('.order_form').on('click', 'input[type=number]', function (){
        let target = event.target;
        orderitem_num =parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if(price_array[orderitem_num]) {
            orderitem_quantity = parseInt(target.value);
            delta_quantity = orderitem_quantity - quantity_array[orderitem_num];
            quantity_array[orderitem_num] = order_total_quantity;

            orderSummaryUpdate(price_array[orderitem_num], delta_quantity)
        };
    });

    console.info('QUA', quantity_array);
    console.info('PRI', price_array);
    console.log(total_forms, order_total_cost, order_total_quantity)

    function orderSummaryUpdate(orderitem_price, delta_quantity){
        delta_cost = orderitem_price * delta_quantity;
        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;
        $('.order_total_cost').html(order_total_cost.toString() + ',00');
        $('.order_total_quantity').html(order_total_quantity.toString());
    }

    function deleteOrderItem(row){

    }
}
