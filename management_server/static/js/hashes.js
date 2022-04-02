
function addNewHash(text, type) {
    const data = { "hash": text, "type": type };

    fetch('/hash', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            window.location.reload();
        })
        .catch((error) => {
            console.error('Error:', error);
            window.location.reload();
        });
}

$("#add-hash-button").click(function () {
    const hash_text = document.getElementById("input-hash-text").value;
    const hash_type = document.getElementById("input-hash-type").value;
    console.log(hash_text);
    console.log(hash_type);
    addNewHash(hash_text, hash_type);
});