const url = location.protocol + '//' + location.host;

function good(good_status, post_id, gooded_id, posted_id) {

    var request = new XMLHttpRequest();

    request.open('GET', url + '/post/good?status=' + good_status + '&post_id=' + post_id + '&user_id=' + gooded_id + '&posted_id=' + posted_id, true);
    request.responseType = 'json';

    request.onload = function() {

        if (request.status === 200) {

            var good_button = document.getElementById('good-' + post_id);

            if (request.response['success']) {

                good_button.innerHTML = ' ' + Number(request.response['count']).toLocaleString();

                create = request.response['create'];

                if (create) {
    
                    good_button.classList.add('liked');
                    good_button.classList.remove('like');
                    good_button.setAttribute('onclick', "good('gooded', " + post_id + ", " + gooded_id + ", " + posted_id + ");");
    
                } else {
    
                    good_button.classList.add('like');
                    good_button.classList.remove('liked');
                    good_button.setAttribute('onclick', "good('good', " + post_id + ", " + gooded_id + ", " + posted_id + ");");

                }

            } else {

                alert('エラーが発生しました。in');

            }
            

        } else {
            alert('エラーが発生しました。');
        }
    }

    request.send();

}

function deletePost(post_id, user_id) {

    var result = window.confirm('この投稿を本当に削除しますか？');

    if (result) {

        var request = new XMLHttpRequest();

        request.open('GET', url + '/post/delete?post_id=' + post_id + '&user=' + user_id, true);
        request.responseType = 'json';

        request.onload = function() {

            if (request.status === 200) {

                if (request.response['success']) {

                    location.reload();

                } else {

                    alert('エラーが発生しました。');
    
                }

            } else {

                alert('エラーが発生しました。');

            }


        }
    }

    request.send();

}

