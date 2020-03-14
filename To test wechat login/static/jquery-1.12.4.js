  $(function () {
            checkLogin();
        })

        $(function () {
            checkLogin();
        });
        function checkLogin() {
            $.ajax({
                url:'{{ url_for('check_login') }}',
                method:'GET',
                dataType:'json',
                success:function (arg) {
                    console.log(arg);
                    checkLogin();

                    if(arg.code === 408){
                        checkLogin();

                    }else if(arg.code === 201){
                        $('#userAvatar').attr('src',arg.avatar);
                        checkLogin();

                    }else if(arg.code === 200){
                        location.href = "{{ url_for('index') }}"
                    }
                }
            })
        }