document.addEventListener('DOMContentLoaded', () => {
    const imgEl = document.getElementById('slideshowImage');

    let data = {};
    try {
        data = JSON.parse(document.getElementById('slideshow-data').textContent);
    } catch (e) {
        console.error("Fehler beim Parsen der slideshow-Daten:", e);
    }

    let urls = data.urls || [];
    let idx = 0;
    let speed = (data.speed || 10) * 1000;
    let cooldown = (data.cooldown || 30) * 1000;

    function showNext() {
        if (!urls.length) return;
        idx = (idx + 1) % urls.length;
        imgEl.src = urls[idx];
    }

    let interval = setInterval(showNext, speed);

    async function reloadSlideshowData() {
        try {
            const resp = await fetch(window.slideshowDataUrl);
            const serverData = await resp.json();

            if (Array.isArray(serverData.urls)) {
                urls = serverData.urls;
                idx = urls.indexOf(imgEl.src);
                if (idx < 0) idx = 0;
            }

            if (!isNaN(serverData.speed)) {
                clearInterval(interval);
                speed = serverData.speed * 1000;
                interval = setInterval(showNext, speed);
            }

            if (!isNaN(serverData.cooldown)) {
                cooldown = serverData.cooldown * 1000;
            }
        } catch (e) {
            console.error("Fehler beim Nachladen:", e);
        }
    }
    reloadSlideshowData();

    setInterval(reloadSlideshowData, cooldown);
});
