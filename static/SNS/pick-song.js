const text_part = document.getElementById("new-post-text");
const song_list_part = document.getElementById("new-post-song-list");
let inner_width;

function switchDisplay(id) {
    inner_width = window.innerWidth;
    console.log(inner_width);
    if (id === 'text') {
        text_part.style.display = "block";
        if (inner_width <= 834) {
            song_list_part.style.display = "none";
        }
    } else {
        if (inner_width <= 834) {
            text_part.style.display = "none";
        }
        song_list_part.style.display = "block";
    }
}

function setSong(song_title, song_id, song_artist, song_album) {
    document.getElementById("title").value = song_name;
    document.getElementById("img").src = song_id;
    document.getElementById("post-id").value = song_id;
    document.getElementById("artist").value = song_artist + " / " + song_album;
}