$(document).ready(function() {
    setTimeout(function() {
        $(".bonfire-pageloader-icon").addClass("bonfire-pageloader-icon-hide");
    }, 500);

    setTimeout(function() {
        $("#bonfire-pageloader").addClass("bonfire-pageloader-hide");
        $("#divResult").css("visibility", "visible");
    }, 750);
})