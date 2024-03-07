const username = document.getElementById('id_username');
const username_check = document.getElementById('username-check');

const password1 = document.getElementById('id_password');
const password2 = document.getElementById('password2');
const pass_length = document.getElementById('pass-length');
const password_check = document.getElementById('password-check');

const email = document.getElementById('id_email');

const url = location.protocol + '//' + location.host;

const signup = document.getElementById('signup');

let username_status = false;
let password_status = false;


function check_username() {

    var request = new XMLHttpRequest();

    username_check.innerHTML = 'データ取得中です。';

    request.open('GET', url + '/check/username/?username=' + username.value, true);
    request.responseType = 'json';

    request.onload = function() {
        if (request.status === 200) {
            if (request.response['exists'] == false) {
                username_status = true;
                username_check.innerHTML = 'このUsernameは使用可能です。';
                username_check.style.color = 'green';
            } else {
                username_status = false;
                username_check.innerHTML = 'このUsernameは使用できません。';
                username_check.style.color = 'red';
            }
        } else {
            username_check.innerHTML = '取得に失敗しました。';
        }
    }

    request.send();

}


function check_password() {

    if (password1.value.length < 8) {
        pass_length.innerHTML = 'パスワードは8文字以上である必要があります。';
        pass_length.style.color = 'red';
        password_status = false;
    } else {
        pass_length.innerHTML = 'パスワードの条件に適合しました。';
        pass_length.style.color = 'green';
        if(password2.value != '') {
            if (password1.value != password2.value) {
                password_check.innerHTML = 'パスワードが一致しません。';
                password_check.style.color = 'red';
                password_status = false;
            } else {
                password_check.innerHTML = 'パスワードが一致しました。';
                password_check.style.color = 'green';
                password_status = true;
            }
        }
    }
}


function check_required() {
    if (password_status && username_status && email.value != '') {
        signup.disabled = false;
    } else {
        signup.disabled = true;
    }
}
