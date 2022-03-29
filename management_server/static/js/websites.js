
function addNewWebsite(text) {
    const data = { "url": text };

    fetch('/website', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            displayReturnData(data);
            //window.location.reload();
        })
        .catch((error) => {
            console.error('Error:', error);
            //window.location.reload();
        });
}

function displayReturnData(data) {
    document.getElementById("public_key").innerText = data["public_key"];
    document.getElementById("secret_key").innerText = data["secret_key"];
    $("#add_website_alert").show();
}

function checkIfCorrect(data) {
    //https://stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url
    var expression = /[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)?/gi;
    var regex = new RegExp(expression);
    if (data.match(regex)) return true;
    return false;
}

$("#add-website-button").click(function () {
    const website_url = document.getElementById("input-website-text").value;
    console.log(website_url);
    if(checkIfCorrect(website_url)) {
        addNewWebsite(website_url);
    }
    //addNewHash(hash_text, hash_type);
});