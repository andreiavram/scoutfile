/**
 * Created by andrei on 10/12/13.
 */

var offset = 0;
var limit = 9;
var stop_flag = true;

function get_photos(url, csrf_token) {
    var stop_flag = true;
//    {"offset": offset, "limit": limit, "tags": $("[name='tags']").val(), "csrfmiddlewaretoken": "{{ csrf_token }}"},
    var data = {"offset" : offset,
            "limit" : limit,
            "csrfmiddlewaretoken" : csrf_token,
            }

    if ($("[name='tags']").length) {
        data.tags = $("[name='tags']").val();
    }



    $.post(url, data,
        function (data) {
            $("#msg").html("<i class = 'icon-search'></i> Am găsit " + data.total_count + " imagini tag-uite cu <strong>" + $("[name='tags']").val() + "</strong>, cele mai recente mai sus");

            $.each(data.data, function (index, element) {
                $("#rezultate-list").append(' \
                                <li class="span3" style="position: relative;"> \
                                    <a href="' + element.url_detail + '" class="thumbnail"> \
                                        <img src="' + element.url_thumb + '"> \
                                    </a> \
                                </li>');

            });
            offset += data.count;
            if (offset < data.total_count) {
                stop_flag = false;
            } else {
                stop_flag = true;
            }
        }, "json");

}