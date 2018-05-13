$(document).ready(function() {
    $("#part2 table:even").css("background-color", "#F9F9F9");
    $("#part2 table:odd").css("background-color", "#FFFFFF");
    var array = $("#part1 table,#part2 table,#part3 table");
    $("#bt").click(function() {
        var m = 0;
        var flag = true;
        for (var i = 0; i < array.size(); i++) {
            var id = array[i].id;
            var val = $('input:radio[name="option' + (i + 1) + '"]:checked').val();
            if (val == null) {
                if (flag) {
                    m = i;
                    flag = false;
                }
                $("#" + id).css("border-color", "#FF9900");
                $("#" + id + " .errormessage").css("visibility", "visible");
            }
        }
        if (!flag) {
            var scroll_offset = $("#" + array[m].id).offset(); //得到pos这个div层的offset，包含两个值，top和left 
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
        if (flag) {
            $("#from1").submit();
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