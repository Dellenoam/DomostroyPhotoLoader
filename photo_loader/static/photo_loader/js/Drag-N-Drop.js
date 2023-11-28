document.addEventListener('DOMContentLoaded', function () {
    const dropArea = document.getElementById('dropArea');
    const fileInput = document.getElementById('fileInput');
    const fileCountElement = document.getElementById('fileCount');
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    dropArea.addEventListener('drop', handleDrop, false);

    fileInput.addEventListener('change', handleFilesFromInput, false);

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight() {
        dropArea.classList.add('active');
    }

    function unhighlight() {
        dropArea.classList.remove('active');
    }

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;

        const fileInput = document.getElementById('fileInput');
        fileInput.files = files;

        if (files.length > 0) {
            fileCounter(files);
        }
    }

    function handleFilesFromInput() {
        const files = fileInput.files;
        if (files.length > 0) {
            fileCounter(files);
        }
    }

    function fileCounter(files) {
        fileCountElement.textContent = `Выбрано файлов: ${files.length}`;

        dropArea.classList.remove('active');
    }
})

function toggleContainer() {
    const container = document.getElementById('upload_form');
    const arrow = document.getElementById('toggleArrow');
    arrow.classList.toggle('arrow_collapsed');
    container.classList.toggle('collapsed');
}