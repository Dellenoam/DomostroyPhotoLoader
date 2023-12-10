function showError() {
    document.getElementById('errorMessage').innerText = '' + error_messages;
    document.getElementById('errorModal').style.display = 'block';
    document.getElementById('blur_bg').style.display = 'block';
}

function closeErrorModal() {
    document.getElementById('errorModal').style.display = 'none';
    document.getElementById('blur_bg').style.display = 'none';
}

setTimeout(closeErrorModal, 10000)

window.addEventListener('load', showError)