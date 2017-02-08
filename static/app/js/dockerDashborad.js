/**
 * Created by king-aric on 16-10-16.
 */

$(function () {
    var addr=variable_win.protocol+"//"+variable_win.host;
    var current=variable_win.uri().substring(addr.length,variable_win.uri().length);

    if (current.substring(current.length-1,current.length)=="#"){
        current=current.substring(0,current.length-1);
    }

    $(".pagination li a ").each(function () {
            var href=this.getAttribute('href');
            if (href !=null){
                $(this).attr('href',current+'?page='+href);
            }
     });

    $(".navbar-header a").each(function(){
         if(current=="/"){
           $(".navbar-header").children("a").first().addClass("active");
             return;
         }
         if (this.getAttribute('href') == current) {
                $(this).attr("style","color: white")
                return;
         }
    });
    bind_docker(0);
    $(".create_container").click(function () {
        $("#image_id").val(this.id)
        $('#create_image').modal({
            keyboard: true
        })
    });
     $(".pull_image_class").click(function () {
                $('#pull_image').modal({
                    keyboard: true
                })
     });
});


//common
function bind_docker(e) {
    if ($("#docker_seleted").val()) {
        writeCookie('docker_server', $("#docker_seleted").val())
        if (e == undefined) {
            window.location.reload()
        }
    }
}

function writeCookie(k, v) {
    var exp = new Date();
    exp.setTime(exp.getTime() + 365 * 24 * 60 * 60 * 1000); //3天过期
    document.cookie = k + "=" + v + ";expires=" + exp.toGMTString() + ";path=/";
}


//images
function create_container(e) {
    $('#create_image').modal('hide');
    if (e && e.getAttribute("create_mode") == 0) {
        $.ajax({
            url: '/containers/create/',
            data: $("#container_form").serialize(),
            type: 'get',
            dataType: 'json',
            success: function (data) {
                if (data.status == 200) {
                    alert(data.msg);
                    window.location.href = data.request
                } else {
                    alert(data.msg)
                }
            },
            error: function (e) {
                console.log(e)
                alert('server error...')
            }
        })
    }else{
       return create_container_shell()
    }
}

function create_container_shell() {
    $.ajax({
        url: '/containers/shell/',
        data: {
            shell: $("#create_shell").val()
        },
        type: 'post',
        dataType: 'json',
        success: function (data) {
            if (data.status == 200) {
                alert(data.msg);
                window.location.href = data.request
            } else {
                alert(data.msg)
            }
        },
        error: function (e) {
            console.log(e)
            alert('server error...')
        }
    })
}


//docker host
function test_host(url, reload) {
    if($("#ip_addr").val()==""){
        alert("地址不能为空.")
        return false;
    }
    $.ajax({
        url: url,
        data: {ip_addr:$("#ip_addr").val()},
        type: 'post',
        dataType: 'json',
        success: function (data) {
            if (data.status == 200) {
                alert(data.msg);
                if (reload) {
                    window.location.reload();
                }
            } else {
                alert(data.msg);
            }
        },
        error: function (e) {
            alert("add error...");
            console.log(e);
        }
    })
}
function create_image(e) {
            $('#pull_image').modal('hide');
            $.ajax({
                url: '/images/pull/',
                data: {image: $("#image_name").val()},
                type: 'get',
                dataType: 'json',
                success: function (data) {
                    if (data.status == 200) {
                        alert(data.msg);
                        window.location.href = data.request
                    } else {
                        alert(data.msg)
                    }
                },
                error: function (e) {
                    console.log(e)
                    alert('server error...')
                }
            })
        }
