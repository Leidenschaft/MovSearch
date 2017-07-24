function user_search(name) {
    ajax({
        type: "POST",
        url: "/dateplace/usersearch",
        dataType: "",
        data: { "name": name},
        beforeSend: function () {
        },
        success: function (msg) {
            arr = msg.split("#");
            var g="小姑娘";
            if( arr[2]=="M"){
                var g="小哥哥";
            }
            if (arr[0] == "ACC") {
                var temp = document.createElement("form");
                if (window.confirm("你要关注"+arr[1]+"这位"+g+"吗？")){
                    ajax({
                        type:"POST",
                        url: "/dateplace/follow",
                        dataType: "",
                        data: { "name": arr[1] },
                        beforeSend: function () { },
                        success: function (msg) {
                            if (msg = "REJECT") {
                                window.location = "";
                                alert("User logged out.");
                            }
                            else {
                                alert("已关注！或许刷新可见。");
                            }
                        },
                        error: function () {
                            alert("error");
                        }
                    })
                }
                else {

                }
            }
            else {
                alert("NO SUCH PERSON");
            }

        },
        error: function () {
            alert("error")
        }
    })
}