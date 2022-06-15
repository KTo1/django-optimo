// window.onload = function () {
$(document).ready(function () {
    console.log('1')

    // basket

    $('.basket_list').on('click', 'input[type="number"]', function (){

        console.log('1')

        let t_href = event.target;

        $.ajax(
            {
                url: '/basket/edit/' + t_href.name + '/' + t_href.value + '/',
                success: function (data){
                   $('.basket_list').html(data.result)
                }
            }
        )
    })


    let total_forms = parseInt($('input[name=orderitems-TOTAL_FORMS]').val())

    $('.order_form').on('click', 'input[type=number]', function (){
        orderSummaryUpdate()
    });

    $('.order_form').on('click', 'input[type=text]', function (){
        orderSummaryUpdate()
    });

    $('select').change(function(){
        product_id = $(event.target).val();
        if(product_id === 0) return false;

        orderitem_id = event.target.name.replace('orderitems-', '').replace('-product', '');

        $.ajax(
            {
                url: '/products/get_price/' + product_id + '/',
                success: function (data){
                   $('input[name=orderitems-' + orderitem_id + '-price]').val(parseFloat(data.result));
                   orderSummaryUpdate();
                }
            }
        )
    });

    function orderSummaryUpdate(){
        let quantity = 0, price = 0, order_total_cost = 0, order_total_quantity = 0;

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
// }
});
