function sendData(data){
    data.csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value
    $.ajax({
        url: window.location,
        type: 'post',
        data: data,
        success: function(result){
            if (result.token){
                localStorage.setItem('token', result.token);
                url = 'http://' + window.location.host + '/servers/';
                console.log(url);
                window.location.href = url;
            }
        }
    });
}

function alreadyIn(){
    token = localStorage.getItem('token');
    data = {'method': 'check_token',
            'token': token};
    result = sendData(data);
}

function signIn(){
    login = $('#login').val();
    password = $('#password').val();
    data = {'method': 'sign_in',
            'login': login,
            'password': password};
    sendData(data);
}

function register(){
    login = $('#login').val();
    password = $('#password').val();
    data = {'method': 'register',
            'login': login,
            'password': password};
    sendData(data);
}
