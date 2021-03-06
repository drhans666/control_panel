$(document).ready(function () {
    $("#section_select").select2({
        tokenSeparators: [',', ' '],
        minimumInputLength: 1,
        minimumResultsForSearch: 5,
        placeholder: 'Select Section',

        ajax: {
            url: '/restapi/sections/',
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
                $.each(data.results, function (i, section) {
                    found.push({
                        id: section.id,
                        text: section.name

                    })
                })
                return {'results': found};
            },
            cache: true
        },
        escapeMarkup: function (markup) { return markup; },
    });
});