$(document).ready(function () {
    $("#manufacturer_select").select2({
        tokenSeparators: [',', ' '],
        minimumInputLength: 1,
        minimumResultsForSearch: 5,
        placeholder: 'Select Manufacturer',

        ajax: {
            url: '/restapi/manufacturers/',
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
                $.each(data.results, function (i, manufacturer) {
                    found.push({
                        id: manufacturer.id,
                        text: manufacturer.name

                    })
                })
                return {'results': found};
            },
            cache: true
        },
        escapeMarkup: function (markup) { return markup; },
    });
});