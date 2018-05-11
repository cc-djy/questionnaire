$(document).ready(function() {
    var array = $("table");

    $("#bt").click(function() {
        for (var i = 0; i < array.size(); i++) {
            var id = array[i].id
            var val = $('input:radio[name="option' + (i + 1) + '"]:checked').val();
            if (val == null) {
                $("#" + id).css("border", "2px solid red");
                $("#" + id + " .errormessage").css("display", "block");
            }
        }

    })

    $(":radio").click(function() {
        var flag = $(this).parents("table").css("border");
        if (flag != null) {
            $(this).parents("table").css("border", "");
            $(this).parents("tr").nextAll().last().css("display", "none");
        }
    })

    $(function() {
        var scroll_offset = $("")
    })
})