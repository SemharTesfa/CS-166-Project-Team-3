const form = document.getElementById("form");
form.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    let data = new FormData();
    console.log(e.target.input.value);
    data.append("body", e.target.input.value);

    const response = await fetch('/submit', {
        method: 'POST',
        body: data
    });
    displayResponse(response);
})

async function displayResponse(response) {
    var div = document.getElementById("response");
    div.setAttribute("style", "border:1px solid black")
    var result = await response.json();
    console.log(result)
    if (response.ok) {
        div.innerHTML = `
        <h1>Response</h1>
        <p>Input OK</p>
        <p>Time: ${result.time}s</p>
        <p>Input: ${result.payload}</p>
        <p>Memory usage: ${result.memory}</p>
        `;
    }
    else if (response.status == 400) {
        div.innerHTML = `
        <p>Bad Input</p>
        <p>Message: ${result.message}</p>
        `;
    }
}