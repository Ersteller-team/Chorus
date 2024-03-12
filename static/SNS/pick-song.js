const text_part = document.getElementById("new-post-text");
const song_list_part = document.getElementById("new-post-song-list");
const search_text = document.getElementById("search-text");
const search_result = document.getElementById("search-result");
const search_result_table = document.getElementById("search-result-table");
const more_button = document.getElementById("more-button");
const song_id = document.getElementById("song-id");
const detail = document.getElementById("detail");
const submit = document.getElementById("submit");
const result_title = document.getElementById("result-title");
const url = location.protocol + '//' + location.host;
const recent_song = search_result_table.innerHTML;
let inner_width, search_word, items;

function switchDisplay(id) {
    inner_width = window.innerWidth;
    if (id === 'text') {
        text_part.style.display = "block";
        song_list_part.style.display = "none";
    } else {
        text_part.style.display = "none";
        song_list_part.style.display = "block";
    }
}

function searchSong(load_times) {

    more_button.innerHTML = 'Loading...';
    more_button.disabled = true;

    if (load_times == 0) {
        more_button.style.display = "none";
        search_result_table.innerHTML = '';
        items = 0;
    }

    search_word = search_text.value;

    if (search_word === "") {
        search_result.innerHTML = '曲を検索してください';
        if (recent_song.match(/<tr>/)) {
            result_title.innerHTML = '最近再生した楽曲';
        }
        search_result_table.innerHTML = recent_song;
        return;
    }

    var request = new XMLHttpRequest();

    request.open('GET', url + '/search/song/?query=' + search_word + '&offset=' + String(load_times * 20), true);
    request.responseType = 'json';

    search_result.innerHTML = 'データ取得中です...';

    request.onload = function() {
        if (request.status === 200) {
            if (request.response['response']['status']['success']) {
                items += request.response['response']['status']['total'];
                search_result.innerHTML = items + '件の楽曲が見つかりました';
                result_title.innerHTML = '';
                for (var i = 0; i < request.response['response']['status']['total']; i++) {
                    var img = request.response['response']['data'][i]['album']['image'];
                    var title = request.response['response']['data'][i]['song']['name'];
                    var id = request.response['response']['data'][i]['song']['id'];
                    var artist = request.response['response']['data'][i]['artist'][0]['name'];
                    for (var j = 1; j < request.response['response']['data'][i]['artist'].length; j++) {
                        artist += ', ' + request.response['response']['data'][i]['artist'][j]['name'];
                    }
                    var album = request.response['response']['data'][i]['album']['name'];
                    search_result_table.innerHTML += `<tr>
                        <td class="song-table-img"><img src="` + img + `" id="img" class="new-post-song-img" alt="` + title + `"></td>
                        <td class="song-table-title"><div class="new-post-song-title-artist">
                            <p class="new-post-song-title dont-new-line">` + title + `</p>
                            <p class="new-post-song-artist dont-new-line">` + artist + ` / ` + album + `</p>
                        </div></td>
                        <td class="song-table-button"><button class="new-post-song-select" type="button" onclick="setSong('` + img + `', '` + title + `', '` + id + `', '` + artist + `', '` + album + `');">選択</button></td>
                    </tr>`;
                    more_button.style.display = "block";
                    more_button.innerHTML = 'More';
                    more_button.setAttribute('onclick', 'searchSong(' + String(load_times + 1) + ')');
                    more_button.disabled = false;
                }
            } else {
                search_result.innerHTML = '楽曲が見つかりませんでした';
            }
        } else {
            search_result.innerHTML = '取得に失敗しました';
        }
    }

    request.send();

}

function setSong(img, song_title, song_id, song_artist, song_album) {

    switchDisplay('text');

    document.getElementById("no-select").innerHTML = "";
    document.getElementById("img").innerHTML = '<img class="new-post-song-img" src="' + img + '"alt="' + song_title + '" />';
    document.getElementById("title").innerHTML = song_title;
    document.getElementById("song-id").value = song_id;
    document.getElementById("artist").innerHTML = song_artist + " / " + song_album;

    post_check();
}

function post_check() {
    if (song_id.value != "" && detail.value != "" && detail.value.length <= 500) {
        submit.disabled = false;
    } else {
        submit.disabled = true;
    }
}
