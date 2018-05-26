$(document).ready(function() {

    var currentIndex = 1;
    var doIndex = 0;
    var paper;
    var part1Length;
    var part2Length;
    var part3Length;
    var totalLength;
     $.get("http://127.0.0.1:8000/",function(data,status){
          paper = data;
          $("#title>span:last").text(data.question_types[0].description);
          part1Length = data.question_types[0].questions.length;
          part2Length = data.question_types[1].questions.length;
          part3Length = data.question_types[2].questions.length;
          totalLength = part1Length+part2Length+part3Length;
          var partNumber = 0;
           for(var j=1,k=0;j<=totalLength;j++,k++) {
                $("#quest" +j+ " > b").text(j+"、"+data.question_types[partNumber].questions[k].title);
                $("#quest" +j+ " label:first").text("A."+data.question_types[partNumber].questions[k].options[0].option_description);
                $("#quest" +j+ " label:last").text("B."+data.question_types[partNumber].questions[k].options[1].option_description);
                if(j==part1Length) {
                    partNumber++;
                    k=-1;
                }
                if(j==part1Length+part2Length) {
                    partNumber++;
                    k=-1;
                }
           }
      });


    $("#start").click(function() {
        $("#index").css("display", "none");
        $("#quest").css("display", "block");
        $(".divQuest:lt(1)").css("display", "block");
        $(".progress").css("display", "block");
        $("html").css("height","100%");
        $("body").css("height","100%");
    })

    //label点击函数
    function clickRadio(obj) {
         if(currentIndex>doIndex) {
            $(":radio").unbind();       //消除label点击
            var parent = $("#"+obj.id).parents(".divQuest");
            parent.fadeOut(200);
            setTimeout(function(){
                if(parent.next().length==0) {
                    return ;
                }
                parent.next().fadeIn(200);
                var id = parent.next().attr("id");
                var id_1 = $("#"+id+" label:first").attr("for");
                var id_2 = $("#"+id+" label:last").attr("for");
                $("#"+id+" label").attr("for","");
                setTimeout(function(){
                    var p = $(".progress-bar").parent().css("width");
                    var length = parseInt(p);
                    doIndex++;
                    currentIndex++;
                    length = length * (doIndex / totalLength);
                    $(".progress-bar").css("width", length + "px");
                    if(doIndex==part1Length) {
                        $("#title>span:first").text("第二部分");
                        $("#title>span:last").text(paper.question_types[1].description);
                    }
                    if(doIndex==part1Length+part2Length) {
                        $("#title>span:first").text("第三部分");
                        $("#title>span:last").text(paper.question_types[2].description);
                    }
                    $(":radio").click(function() {
                        clickRadio(this);
                    })
                    $("#"+id+" label:first").attr("for",id_1);
                    $("#"+id+" label:last").attr("for",id_2);
                },200)
            },200);
         }
    }

    $(":radio").click(function() {
        clickRadio(this);
    })

    //防止用户多次点击
    var _timer = {};
    function delay_till_last(id,fn,wait) {
        if(_timer[id]) {
            window.clearTimeout(_timer[id]);
            delete _timer[id];
        }

        return _timer[id] = window.setTimeout(function() {
                    fn();
                    delete _timer[id];
                }, wait);
    }

    //返回上一次
    function backLast() {
         if(currentIndex>1) {
            $("#butn1").unbind();   //点击后消除点击效果，等上一题完全显示后再添加点击事件
            $("#butn2").attr("disabled","true");
            $("#butn3").attr("disabled","true");
             var divObj = $("#quest"+currentIndex);
             divObj.fadeOut(200);
             setTimeout(function(){
                 divObj.prev().fadeIn(200);
                 setTimeout(function() {
                      currentIndex--;
                      $("#butn1").click(function(){
                          backLast();
                      })
                      $("#butn2").removeAttr("disabled");
                      $("#butn3").removeAttr("disabled");
                 },200);
             },200)
        }
    }

    //返回下一题
    function backNext() {
        if(currentIndex<=doIndex) {
            $("#butn2").unbind();
            $("#butn1").attr("disabled","disabled");
            $("#butn3").attr("disabled","disabled");
            var divObj = $("#quest"+currentIndex);
            divObj.fadeOut(200);
            setTimeout(function(){
                divObj.next().fadeIn(200);
                setTimeout(function() {
                    currentIndex++;
                    $("#butn2").click(function(){
                        backNext();
                    })
                    $("#butn1").removeAttr("disabled");
                    $("#butn3").removeAttr("disabled");
                },200);
            },200)
        }
    }

    //跳转到未答题
    function toDoIndex() {
        if(currentIndex<=doIndex) {
             $("#butn1").attr("disabled","disabled");
             $("#butn2").attr("disabled","disabled");
             $("#quest"+currentIndex).fadeOut(200);
             setTimeout(function(){
                 $("#quest"+(doIndex+1)).fadeIn(200);
                 setTimeout(function(){
                    currentIndex=doIndex+1;
                    $("#butn1").removeAttr("disabled");
                    $("#butn2").removeAttr("disabled");
                 },200);
             },200)
        }
    }


    $("#butn1").click(function(){
        backLast();
    })

    $("#butn2").click(function(){
        backNext();
    })

    $("#butn3").click(function(){
        toDoIndex();
    })

    $("#tijiao").click(function() {
        var val = $('input:radio[name="option' + 1 + '"]:checked').val();
        alert(val);
    })

})