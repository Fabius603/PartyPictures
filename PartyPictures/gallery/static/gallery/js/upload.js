document.addEventListener("DOMContentLoaded", function () {
    const fileInput         = document.getElementById('fileInput');
    const preview           = document.getElementById('preview');
    const previewBox        = document.getElementById('previewContainer');
    const cancelBtn         = document.getElementById('cancelBtn');
    const uploadButton      = document.querySelector('.upload-button');
    const form              = document.getElementById('uploadForm');
    const loadingOverlay    = document.getElementById('loadingOverlay');
    const cameraIcon        = document.getElementById('cameraIcon');

    fileInput.addEventListener('change', () => {
        const file = fileInput.files[0];
        if (!file) return;

        const url = URL.createObjectURL(file);
        preview.src = url;
        previewBox.style.display = 'flex';
        uploadButton.style.display = 'none';
        cameraIcon.style.display = 'none';

        // Layout nach oben verschieben
        form.style.justifyContent = 'flex-start';
    });

    cancelBtn.addEventListener('click', () => {
        fileInput.value = '';
        previewBox.style.display = 'none';
        uploadButton.style.display = 'inline-block';
        cameraIcon.style.display = 'block';

        // Layout wieder mittig
        form.style.justifyContent = 'center';
    });

    form.addEventListener('submit', () => {
        loadingOverlay.style.display = 'flex';
    });

});
