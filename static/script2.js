const loader = document.querySelector('.lyricity-loader');
function spinner() {
    loader.style.display = 'block';
}

function retrieveLyric() {
    const select = document.querySelector('#select-artist');
    if (select.value !== '') {
        const selectedArtist = select.value;
        const url = `${window.location.origin}/artist/generate/${select.value}`;
        const xhr = new XMLHttpRequest();

        xhr.addEventListener('progress', spinner);

        xhr.onreadystatechange = function () {
            loader.style.display = 'none';
            if (this.readyState !== 4) return;

            if (this.status === 200) {
                const data = JSON.parse(this.responseText);
                if (data.error)
                    return;

                const lyricElem = document.querySelector('#lyricity-lyric-text');
                lyricElem.textContent = data.lyric;
            }
        };

        xhr.open('GET', url, true);
        xhr.send();
    }
}

async function retrieveLyricRandom() {
    const url = `${window.location.origin}/artist/generate_random`;
    const xhr = new XMLHttpRequest();

    xhr.addEventListener('progress', spinner);

    xhr.onreadystatechange = function () {
        loader.style.display = 'none';
        if (this.readyState !== 4) return;

        if (this.status === 200) {
            const data = JSON.parse(this.responseText);
            if (data.error)
                return;

            const lyricElem = document.querySelector('#lyricity-lyric-text');
            lyricElem.textContent = data.lyric;
        }
    };

    xhr.open('GET', url, true);
    xhr.send();
}

document.querySelector('#artist-generate').addEventListener('click', retrieveLyric);
document.querySelector('#random-artist').addEventListener('click', retrieveLyricRandom);