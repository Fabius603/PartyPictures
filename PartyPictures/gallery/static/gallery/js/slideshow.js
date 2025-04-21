document.addEventListener('DOMContentLoaded', () => {
    const imgEl = document.getElementById('slideshowImage');
    let urls = JSON.parse(document.getElementById('slideshow-data').textContent);
    let idx = 0;
    let speed = 10000; // Default = 10s
    let cooldown = 30000 // Default = 30s

    function showNext() {
        if (!urls.length) return;
        idx = (idx + 1) % urls.length;
        imgEl.src = urls[idx];
    }

    // Bildwechsel alle X Sekunden
    let interval = setInterval(showNext, speed);

    // Daten vom Server nachladen (inkl. Geschwindigkeit)
    async function reloadSlideshowData() {
        try {
            const resp = await fetch(window.slideshowDataUrl);
            const data = await resp.json();
            if (Array.isArray(data.urls)) {
                urls = data.urls;
                idx = urls.indexOf(imgEl.src);
                if (idx < 0) idx = 0;
            }
            if (!isNaN(data.speed)) {
                clearInterval(interval);
                speed = data.speed * 1000;
                interval = setInterval(showNext, speed);
            }
            if (!isNaN(data.cooldown)) {
                clearInterval(interval);
                cooldown = data.cooldown * 1000;
                interval = setInterval(showNext, cooldown);
            }
        } catch (e) {
            console.error("Fehler beim Nachladen:", e);
        }
    }

    // Nachladen
    setInterval(reloadSlideshowData, cooldown);
});
