// Call the dataTables jQuery plugin
$(document).ready(function () {

    $("table[name='dataTableOrder']").dataTable( {
        "ordering": true,
        "order": [[ 0, 'desc' ]]
    });

    $("table[name='dataTableActions']").dataTable( {
        "ordering": true,
        "order": [[ 2, 'asc' ], [ 4, 'desc' ]]
    });

    $('#dataTable').DataTable();

});
