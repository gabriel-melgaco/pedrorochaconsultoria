//envio de arquivos database
document.getElementById('downloadDatabase').addEventListener('submit', function(event) {
    event.preventDefault(); 

    const password = document.getElementById('password').value;

    fetch(`/download_database`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ password: password })
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        } else {
            return response.json().then(data => { throw new Error(data.message); });
        }
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'dados.db';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
        document.getElementById('downloadDatabase').reset();
    })
    .catch(error => console.error('Erro ao enviar dados:', error));
});

