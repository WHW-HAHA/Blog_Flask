
        var Highlight = {
            arr : [],
            init : function (ops){
                this.arr[ops.id] = {
                    id : ops.id,
                    arr : ops.arr
                }
                this.show(this.arr[ops.id]);
            },
            show : function (obj){
                obj.html = document.getElementById(obj.id).innerHTML;
                for (var i = 0 ; i < obj.arr.length ; i ++) {
                    // 全局匹配 替换
                    var reg = new RegExp(obj.arr[i],'g');
                    obj.html = obj.html.replace(reg,"<span class='Highlight'>"+obj.arr[i]+"</span>");
                }
                document.getElementById(obj.id).innerHTML = obj.html;
            }
        }
        window.onload = function (){
            // 使用方法
            // id 必须
            // 默认为id 高亮内容添加class为 Highlight span 标签包裹，直接在style中写样式即可
            Highlight.init({id:"title",arr:["content"]});
            Highlight.init({id:"subtitle",arr:["content"]});
            Highlight.init({id:"content",arr:["content"]});
            Highlight.init({id:"header",arr:["no"]});
        }
