const loader = document.querySelector('.lyricity-loader')

function retrieveLyric() {
    loader.style.display = 'block';
    const select = document.querySelector('#select-artist');
    if (select.value !== '') {
        const selectedArtist = select.value;
        const lineNumber = document.querySelector('#js-line-number').value || 20;
        const url = `${window.location.origin}/artist/generate/${select.value}/${lineNumber}`;

        fetch(url)
            .then((response) => response.json())
            .then((data) => {
                loader.style.display = 'none';
                if (data.error)
                    return;

                const artistElem = document.querySelector('#lyricity-artist-text');
                const wrapper = document.querySelector('.lyricity-wrapper');
                const lyricElem = document.querySelector('#lyricity-lyric-text');
                wrapper.style.display = 'block'
                artistElem.textContent = data.artist;
                lyricElem.textContent = data.lyric;
            })
    }
    else {
        loader.style.display = 'none';
    }
}

function retrieveLyricRandom() {
    loader.style.display = 'block';
    const lineNumber = document.querySelector('#js-line-number').value || 20;
    const url = `${window.location.origin}/artist/generate_random/${lineNumber}`;

    fetch(url)
        .then((response) => response.json())
        .then((data) => {
            loader.style.display = 'none';
            if (data.error)
                return;
            
            const artistElem = document.querySelector('#lyricity-artist-text');
            const wrapper = document.querySelector('.lyricity-wrapper');
            const lyricElem = document.querySelector('#lyricity-lyric-text');
            wrapper.style.display = 'block'
            artistElem.textContent = data.artist;
            lyricElem.textContent = data.lyric;
        })
}

document.querySelector('#artist-generate').addEventListener('click', retrieveLyric);
document.querySelector('#random-artist').addEventListener('click', retrieveLyricRandom);