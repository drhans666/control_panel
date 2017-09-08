$(document).ready(function () {
    $("#item_select").select2({
        tokenSeparators: [',', ' '],
        minimumInputLength: 1,
        minimumResultsForSearch: 5,
        placeholder: 'Select Item',

        ajax: {
            url: '/restapi/items/',
            dataType: "json",
            type: "GET",
            data: function (params) {

                var queryParameters = {
                    search: params.term
                }
                return queryParameters;
            },
            processResults: function (data) {
                var found = []
                $.each(data.results, function (i, item) {
                    found.push({
                        id: item.id,
                        text: item.name + ' ' + item.manufacturer

                    })
                })
                return {'results': found};
            },
            cache: true
        },
        escapeMarkup: function (markup) { return markup; },
    });
});