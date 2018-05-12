$(document).ready(function() {
    $("#part2 table tr>th:even").css("background-color", "#F9F9F9");
    $("#part2 table tr>th:odd").css("background-color", "#FFFFFF");
    var array = $("#part1 table,#part3 table");
    $("#bt").click(function() {
        var j = 0;
        var flag = true;
        for (var i = 0; i < array.size(); i++) {
            var id = array[i].id
            var val = $('input:radio[name="option' + (i + 1) + '"]:checked').val();
            if (val == null) {
                if (flag) {
                    j = i;
                    flag = false;
                }
                $("#" + id).css("border-color", "red");
                $("#" + id + " .errormessage").css("visibility", "visible");
            }
        }
        if (!flag) {
            var scroll_offset = $("#" + array[j].id).offset(); //得到pos这个div层的offset，包含两个值，top和left 
            $("body,html").animate({
                scrollTop: scroll_offset.top //让body的scrollTop等于pos的top，就实现了滚动 
            }, 200);
            $(".scrolltop").show();
            $(".scrolltop").click(function() {
                $("html, body").animate({
                    scrollTop: $(document).height()
                }, 200);
                $(".scrolltop").hide();
            });
        }
    });

    $(":radio").click(function() {
        var flag = $(this).parents("table").css("border");
        if (flag != null) {
            $(this).parents("table").css("border-color", "#F7F7F7");
            $(this).parents("tr").nextAll().last().css("visibility", "hidden");
        }
    });

})