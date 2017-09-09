$(document).ready(function () {
    $("#user_select").select2({
        tokenSeparators: [',', ' '],
        minimumInputLength: 1,
        minimumResultsForSearch: 5,
        placeholder: 'Select User',

        ajax: {
            url: '/restapi/users/',
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
                $.each(data.results, function (i, user) {
                    found.push({
                        id: user.id,
                        text: user.username

                    })
                })
                return {'results': found};
            },
            cache: true
        },
        escapeMarkup: function (markup) { return markup; },
    });
});