var place = new Array("Dummy_place", "模型店", "桌游店", "茶饮店", "电玩店", "卡拉OK", "服装店", "中古店", "旧书店", "娃娃机", "女仆咖啡厅", "庭院书店", "洋馆西餐厅", "咖啡馆", "LiveHouse", "外文书店", "剧场", "音乐厅", "美术馆", "电影院", "都市公园", "研究所", "博物馆", "图书馆", "滑冰场", "羽毛球场", "足球场", "篮球场", "远洋码头", "海中孤岛", "跨海大桥", "景观湖泊", "海岬", "沙滩公园", "山路", "游乐场", "赛车场", "神社", "河岸公园", "植物园", "动漫展", "废弃车站")
var val = new Array(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
function button_next(form) {
    num_div = document.getElementById("question_number");
    num = parseInt(num_div.innerHTML);
    level = parseInt(form.level.value);
    val[num] = level;
    if (num == 1) {
        prv_button = document.getElementById("previous");
        prv_button.removeAttribute("disabled");
    }
    if (num == 40) {
        next_button = document.getElementById("next");
        next_button.innerHTML = "提交并查看结果";
    }
    if (num == 41) {
        var temp = document.createElement("form");
        temp.action = "/dateplace/result";
        temp.method = "post";
        var s="";
        var i=0;
        for (i=0;i<val.length;i=i+1){
            s=s+val[i].toString();
        }
        var opt = document.createElement("textarea");
        opt.name = "r_length";
        opt.value = val.length.toString();
        temp.appendChild(opt);
        var opt = document.createElement("textarea");
        opt.name = "r_value";
        opt.value = s;
        temp.appendChild(opt);
        document.body.appendChild(temp);
        temp.submit();
        return temp;
    }
    radio_opt = document.getElementById("Highest");
    radio_opt.checked = false;
    radio_opt = document.getElementById("High");
    radio_opt.checked = false;
    radio_opt = document.getElementById("Medium");
    radio_opt.checked = false;
    radio_opt = document.getElementById("Low");
    radio_opt.checked = false;
    radio_opt = document.getElementById("Lowest");
    radio_opt.checked = false;
    radio_opt = document.getElementById("Zero");
    radio_opt.checked = false;
    num = num + 1;
    picture = document.getElementById("picture");
    path1 = "/static/image/";
    path2 = ".jpg";
    path = path1 + num.toString() + path2;
    picture.setAttribute("src", path);
    num_div.innerHTML = num.toString();
    place_div = document.getElementById("question_place");
    place_div.innerHTML = place[num];
    switch (val[num]) {
        case 5:
            radio_opt = document.getElementById("Highest");
            radio_opt.checked = true;
            break;
        case 4:
            radio_opt = document.getElementById("High");
            radio_opt.checked = true;
            break;
        case 3:
            radio_opt = document.getElementById("Medium");
            radio_opt.checked = true;
            break;
        case 2:
            radio_opt = document.getElementById("Low");
            radio_opt.checked = true;
            break;
        case 1:
            radio_opt = document.getElementById("Lowest");
            radio_opt.checked = true;
            break;
        case 0:
            radio_opt = document.getElementById("Zero");
            radio_opt.checked = true;
            break;
        default:
            break;
    }
}

function button_previous(form) {
    num_div = document.getElementById("question_number");
    num = parseInt(num_div.innerHTML);
    level = parseInt(form.level.value);
    val[num] = level;
    if (num == 2) {
        prv_button = document.getElementById("previous");
        prv_button.setAttribute("disabled","disabled");
    }
    if (num == 41) {
        next_button = document.getElementById("next");
        next_button.innerHTML = "下一题";
    }
    radio_opt = document.getElementById("Highest");
    radio_opt.checked = false;
    radio_opt = document.getElementById("High");
    radio_opt.checked = false;
    radio_opt = document.getElementById("Medium");
    radio_opt.checked = false;
    radio_opt = document.getElementById("Low");
    radio_opt.checked = false;
    radio_opt = document.getElementById("Lowest");
    radio_opt.checked = false;
    radio_opt = document.getElementById("Zero");
    radio_opt.checked = false;
    num = num - 1;
    picture = document.getElementById("picture");
    path1 = "/static/image/";
    path2 = ".jpg";
    path = path1 + num.toString() + path2;
    picture.setAttribute("src", path);
    num_div.innerHTML = num.toString();
    place_div = document.getElementById("question_place");
    place_div.innerHTML = place[num];
    switch (val[num]) {
        case 5:
            radio_opt = document.getElementById("Highest");
            radio_opt.checked = true;
            break;
        case 4:
            radio_opt = document.getElementById("High");
            radio_opt.checked = true;
            break;
        case 3:
            radio_opt = document.getElementById("Medium");
            radio_opt.checked = true;
            break;
        case 2:
            radio_opt = document.getElementById("Low");
            radio_opt.checked = true;
            break;
        case 1:
            radio_opt = document.getElementById("Lowest");
            radio_opt.checked = true;
            break;
        case 0:
            radio_opt = document.getElementById("Zero");
            radio_opt.checked = true;
            break;
        default:
            break;
    }
}