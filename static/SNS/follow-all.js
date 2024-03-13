const url = location.protocol + '//' + location.host;
const button = document.getElementById("follow-all");
const csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

console.log(csrf_token);


function follow_all() {

    continue_follow = window.confirm('全曲フォローします\nよろしいですか？');

    if (!continue_follow) {
        return;
    }

    alert('全曲フォローを開始します\nページを移動しないでください');

    button.disabled = true;

    button.innerHTML = 'Progress...';

    var request = new XMLHttpRequest();

    var body = {
        'csrfmiddlewaretoken': csrf_token,
        'page': location.href,
    };

    request.open('POST', url + '/follow/all/', true);
    request.responseType = 'json';
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('X-CSRFToken', csrf_token);

    request.onload = function() {

        if (request.status == 200) {

            if (request.response['success']) {
                alert('全曲フォローしました\n今後もボタンが表示されますが、フォロー解除は行えません\nご了承ください');
                button.innerHTML = 'フォロー済み';
            } else {
                button.innerHTML = 'フォロー失敗';
                alert('エラーが発生しました');
                location.reload();
            }

        } else {
            button.innerHTML = 'フォロー失敗';
            alert('エラーが発生しました');
            location.reload();
        }

    }

    request.send(JSON.stringify(body));

}
