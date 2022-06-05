$(document).ready(function () {
    console.log('t')
    $('#dataTableOrders').dataTable( {
        "ordering": true,
        "order": [[ 0, 'desc' ]]
    } );

    $('#dataTableActions').dataTable( {
        "ordering": true,
        "order": [[ 2, 'asc' ], [ 4, 'desc' ]]
    } );
});


// window.onload = function (){
//
// }