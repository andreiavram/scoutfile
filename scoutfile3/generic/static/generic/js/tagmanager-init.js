$(document).ready(function () {
    $(".tm-input").each(function (index) {

        var field_name = $(this).data("field-name");
        var ajax_url = $(this).data("ajax-url");

        console.log($(this));
        $(this).tagsManager({
            hiddenTagListName: field_name,
            tagsContainer: "#" + field_name + "_tag_container",
        });

        $(this).typeahead({
            name: 'tags',
            limit: 20,
            remote: ajax_url + "?q=%QUERY"
        }).on('typeahead:selected', function (e, d) {
                tagApi.tagsManager("pushTag", d.value);
            });
    });

});