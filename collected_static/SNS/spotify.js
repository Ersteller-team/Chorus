const text_part = document.getElementById("new-post-text");
const song_list_part = document.getElementById("new-post-song-list");
const search_text = document.getElementById("search-text");
const search_result = document.getElementById("search-result");
const search_result_table = [
    document.getElementById("search-result-table-tracks"),
    document.getElementById("search-result-table-artists"),
    document.getElementById("search-result-table-albums"),
    document.getElementById("search-result-table-playlists"),
];
const url_type = {
    'track': 'song',
    'playlist': 'playlist',
    'album': 'album',
    'artist': 'artist'
}
const more_button = document.getElementById("more-button");
const song_id = document.getElementById("song-id");
const detail = document.getElementById("detail");
const submit = document.getElementById("submit");
const url = location.protocol + '//' + location.host;
const search_type = ['tracks', 'artists', 'albums', 'playlists', 'recent'];
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

function display(page) {

    for (let i = 0; i < search_type.length; i++) {

        if (page === i) {

            document.getElementById('search-button-' + search_type[i]).classList.add("button-select");
            document.getElementById('search-result-table-' + search_type[i]).style.display = "";

        } else {

            document.getElementById('search-button-' + search_type[i]).classList.remove("button-select");
            document.getElementById('search-result-table-' + search_type[i]).style.display = "none";

        }

    }

}

function searchSong(load_times) {

    more_button.innerHTML = 'Loading...';
    more_button.disabled = true;

    search_word = search_text.value;

    var index = search_word.indexOf("spotify.com");

    if (index != -1) {
    
        var id = "";
        var i = 0;
        location_path = search_word.split('/');

        while (location_path.slice(-1)[0][i] != '?' && i < location_path.slice(-1)[0].length) {
            id += location_path.slice(-1)[0][i];
            i++;
        }

        location.href = url + '/search/' + url_type[location_path.slice(-2)[0]] + '/' + id;

        search_result.innerHTML = 'リダイレクトしています...';

        return;

    }

    if (load_times == 0) {
        more_button.style.display = "none";
        for (let i = 0; i < search_type.length; i++) {
            search_result_table[i].innerHTML = '';
        }
        items = 0;
    }

    if (search_word === "") {
        search_result.innerHTML = '検索ワードを入力してください';
        return;
    }

    var request = new XMLHttpRequest();

    search_result.innerHTML = 'データ取得中です...';

    request.open('GET', url + '/search/any/?query=' + search_word + '&offset=' + String(load_times * 20), true);
    request.responseType = 'json';

    request.onload = function() {
        if (request.status === 200) {
            if (request.response['response']['status']['success']) {
                search_result.innerHTML = '';

                res_data = request.response['response']['data'];

                for (var i = 0; i < res_data['tracks'].length; i++) {

                    var img = res_data['tracks'][i]['album']['image'];
                    var id = res_data['tracks'][i]['track']['id'];
                    var title = res_data['tracks'][i]['track']['name'];
                    var artist = res_data['tracks'][i]['artist'][0]['name'];
                    for (var j = 1; j < res_data['tracks'][i]['artist'].length; j++) {
                        artist += ', ' + res_data['tracks'][i]['artist'][j]['name'];
                    }
                    var album = res_data['tracks'][i]['album']['name'];
                    
                    search_result_table[0].innerHTML += `<tr>
                        <td class="song-table-img"><img src="` + img + `" id="img" class="new-post-song-img" alt="` + title + `"></td>
                        <td class="song-table-title">
                            <div class="search-song-title-artist new-post-song-title-artist">
                                <a href="` + url + `/search/song/` + id + `"><p class="new-post-song-title dont-new-line">` + title + `</p>
                                <a href="` + url + `/search/song/` + id + `"><p class="new-post-song-artist dont-new-line">` + artist + ` / ` + album + `</p>
                            </div>
                        </td>
                    </tr>`;

                }

                for (var i = 0; i < res_data['artists'].length; i++) {

                    var img = res_data['artists'][i]['artist']['image'];
                    var id = res_data['artists'][i]['artist']['id'];
                    var artist = res_data['artists'][i]['artist']['name'];
                    
                    search_result_table[1].innerHTML += `<tr>
                        <td class="song-table-img"><img src="` + img + `" id="img" class="new-post-song-img" alt="` + artist + `"></td>
                        <td class="song-table-title">
                            <div class="search-song-title-artist new-post-song-title-artist">
                                <a href="` + url + `/search/artist/` + id + `"><p class="new-post-song-title dont-new-line">` + artist + `</p>
                            </div>
                        </td>
                    </tr>`;

                }

                for (var i = 0; i < res_data['albums'].length; i++) {

                    var img = res_data['albums'][i]['album']['image'];
                    var id = res_data['albums'][i]['album']['id'];
                    var album = res_data['albums'][i]['album']['name'];
                    var artist = res_data['albums'][i]['artist'][0]['name'];
                    for (var j = 1; j < res_data['albums'][i]['artist'].length; j++) {
                        artist += ', ' + res_data['albums'][i]['artist'][j]['name'];
                    }
                    
                    search_result_table[2].innerHTML += `<tr>
                        <td class="song-table-img"><img src="` + img + `" id="img" class="new-post-song-img" alt="` + album + `"></td>
                        <td class="song-table-title">
                            <div class="search-song-title-artist new-post-song-title-artist">
                                <a href="` + url + `/search/album/` + id + `"><p class="new-post-song-title dont-new-line">` + album + `</p>
                                <a href="` + url + `/search/album/` + id + `"><p class="new-post-song-artist dont-new-line">` + artist + `</p>
                            </div>
                        </td>
                    </tr>`;

                }

                for (var i = 0; i < res_data['playlists'].length; i++) {

                    var img = res_data['playlists'][i]['playlist']['image'];
                    var id = res_data['playlists'][i]['playlist']['id'];
                    var name = res_data['playlists'][i]['playlist']['name'];
                    
                    search_result_table[3].innerHTML += `<tr>
                        <td class="song-table-img"><img src="` + img + `" id="img" class="new-post-song-img" alt="` + name + `"></td>
                        <td class="song-table-title">
                            <div class="search-song-title-artist new-post-song-title-artist">
                                <a href="` + url + `/search/playlist/` + id + `"><p class="new-post-song-title dont-new-line">` + name + `</p>
                            </div>
                        </td>
                    </tr>`;

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
