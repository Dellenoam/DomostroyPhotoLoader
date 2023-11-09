function handle_user_images(event) {
    event.preventDefault();

    for (const element of form.elements) {
        if (element.type === 'radio' && element.id.startsWith('replace_') && element.checked) {
            const file_name = element.name;
            const file_data = form['user_' + file_name].value;

            void fetch_images_to_server(file_name, file_data);
        }
    }
}

async function fetch_images_to_server(file_name, file_data) {
    const csrf_token = getCookie('csrftoken')
    await fetch(files_selection_form_submit_url, {
        method: 'POST',
        body: JSON.stringify({
            'file_name': file_name,
            'file_data': file_data,
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,
        },
    });
}

function getCookie(name) {
    const cookieParts = document.cookie.split(';');

    for (const part of cookieParts) {
        const cookiePair = part.split('=');
        const cookieName = cookiePair[0].trim();

        if (cookieName === name) {
            return decodeURIComponent(cookiePair[1]);
        }
    }

    return null;
}

const form = document.getElementById('files_selection_form')
form.addEventListener('submit', handle_user_images)
