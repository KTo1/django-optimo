$(document).ready(function () {
    console.log('t')
    $("table[name='dataTableOrder']").dataTable( {
        "ordering": true,
        "order": [[ 0, 'desc' ]]
    });

    $("table[name='dataTableActions']").dataTable( {
        "ordering": true,
        "order": [[ 2, 'asc' ], [ 4, 'desc' ]]
    });
});


// window.onload = function (){
//
// }