$(document).ready(function () {
    $("#category_select").select2({
        tokenSeparators: [',', ' '],
        minimumInputLength: 1,
        minimumResultsForSearch: 5,
        multiple: true,
        placeholder: 'Select Categories',


        ajax: {
            url: '/restapi/categories/',
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
                $.each(data.results, function (i, category) {
                    found.push({
                        id: category.id,
                        text: category.name

                    })
                })
                return {'results': found};
            },
            cache: true
        },
        escapeMarkup: function (markup) { return markup; },
    });
});