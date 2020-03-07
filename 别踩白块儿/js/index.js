    // 工具封装
    // 根据id来获取元素
    function $(id) {
        return document.getElementById(id);
    }

    // 创建div, className是其类名
    function creatediv(className) {
        var div = document.createElement('div');
        div.className = className;
        return div;
    }
    var clock = null;
    var state = 0;
    var speed = 6;
    var flag = false;//标志位：判断游戏是否开始


    //点击开始游戏按钮 开始游戏
    function start() {
        if(!flag) {
            init();
        } else {
            alert('游戏已经开始，无须再次点击！')
        }
    }

    /*
     *    初始化 init
     */
    function init() {
        flag = true;
            for (var i = 0; i < 4; i++) {//先造四行出来
                createrow();
            }
 
            // 添加onclick事件
            $('main').onclick = function (ev) {//onclick 这个事件发生后会向回调函数传递一个MouseEvent（鼠标事件）
                ev = ev || event //这个event是什么意思？好像是为兼容IE浏览器
                judge(ev);
            }

            // 定时器 每30毫秒调用一次move()
            clock = window.setInterval('move()', 30);
        }

    function createrow() {
        var con = $('con');//确定游戏窗口的位置
        var row = creatediv('row'); //创建div className=row
        var arr = creatcell(); //定义div cell的类名,其中一个为cell black

        con.appendChild(row); // 添加row为con的子节点，相当于在窗口中添加了一行

        for (var i = 0; i < 4; i++) {
            row.appendChild(creatediv(arr[i])); //添加row的子节点 cell
        }

        if (con.firstChild == null) {//这一块的目的始终添加在con节点的第一行，因为新行要在上面出现
            con.appendChild(row);
        } else {
            con.insertBefore(row, con.firstChild);
        }
    }
    // 创建一个类名的数组，其中一个为cell black, 其余为cell
    function creatcell() {
        var temp = ['cell', 'cell', 'cell', 'cell', ];
        var i = Math.floor(Math.random() * 4);//随机产生黑块的位置 Math.random()函数参数 0~3的随机数
        temp[i] = 'cell black';
        return temp;
    }


    // 判断是否点击黑块、白块
    function judge(ev) {
        if(ev.target.className.indexOf('black') == -1 && ev.target.className.indexOf('cell') !== -1) {//MouseEvent事件下边有target属性，该属性可以读取className（是一个字符串），indexOf方法是字符串对象的一个方法，用来定位子串位置，-1表示不存在。
            ev.target.parentNode.pass1 = 1; //定义属性pass，表示此行row的白块已经被点击，pass属性用来最后over函数判断
        }

        if (ev.target.className.indexOf('black') !== -1) {//点击目标元素 类名中包含 black 说明是黑块
            ev.target.className = 'cell';//把className改成cell，在css渲染的时候就是白色了
            ev.target.parentNode.pass = 1; //定义属性pass，表明此行row的黑块已经被点击
            score();
        }


    }

// 判断游戏是否结束

function over() {
    var rows = con.children;
    if ((rows.length == 5) && (rows[rows.length - 1].pass != 1)) {
        fail();
    }
    for(let i = 0; i < rows.length; i++){
        if(rows[i].pass1 == 1) {
            fail();
        }
    }

}

    // 游戏结束
    function fail() {
        clearInterval(clock);//清除时钟计数器
        flag = false;//清除游戏开始计数器，响应下一次“开始”点击
        confirm('你的最终得分为 ' + parseInt($('score').innerHTML)); 
        var con = $('con');
        con.innerHTML =  "";
        $('score').innerHTML = 0;
        con.style.top = '-408px';

    }

    // 创造一个<div class="row">并且有四个子节点<div class="cell">
   




    //移动函数，实际上就是不断调整con元素的顶部位置
    function move() {
        var con = $('con');
        var top = parseInt(window.getComputedStyle(con, null)['top']);

        if (speed + top > 0) {
            top = 0;
        } else {
            top += speed;
        }
        con.style.top = top + 'px';//不断移动top值，使它动起来
        over();
        if (top == 0) {
            createrow();
            con.style.top = '-102px';
            delrow();
        } 
    }


    // 加速函数
    function speedup() {
        speed += 2;
        if (speed == 20) {
            alert('你超神了');
        }
    }

    //删除最后一行
    function delrow() {
        var con = $('con');
        if (con.childNodes.length == 6) {
            con.removeChild(con.lastChild);
        }
    }

    // 记分
    function score() {
        var newscore = parseInt($('score').innerHTML) + 1;//分数加一
        $('score').innerHTML = newscore;//修改分数
        if (newscore % 10 == 0) {//当分数是10 的倍数时使用加速函数，越来越快
            speedup();
        }
    }
