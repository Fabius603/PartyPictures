// Verlaufseintrag ersetzen → verhindert "Zurück" auf dieselbe Seite
if (window.history.replaceState) {
    window.history.replaceState(null, "", window.location.href);
}
