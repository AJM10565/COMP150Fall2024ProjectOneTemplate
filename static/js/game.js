// When the game starts, send a POST request to the backend
function startGame() {
    fetch("/start", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);  // Log the response from the backend
        // Display the riddle and options on the page
        displayRiddle(data.riddle, data.options);
    })
    .catch(error => console.error('Error:', error));
}
function displayRiddle(riddle, options) {
    const riddleElement = document.getElementById("riddle");
    const optionsElement = document.getElementById("options");

    riddleElement.innerText = riddle;  // Display the riddle
    optionsElement.innerHTML = "";  // Clear previous options

    options.forEach((option, index) => {
        const optionElement = document.createElement("button");
        optionElement.innerText = option;
        optionElement.onclick = function() { makeChoice(index); };  // Handle option selection
        optionsElement.appendChild(optionElement);
    });
}
function makeChoice(choiceIndex) {
    fetch("/choice", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ choice: choiceIndex })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);  // Log the response from the backend
        // Display the result and next riddle
        if (data.game_over) {
            alert("Game Over! You've finished all the riddles.");
        } else {
            alert(data.message);  // Display correct/incorrect message
            displayRiddle(data.next_riddle, data.next_options);  // Show the next riddle
        }
    })
    .catch(error => console.error('Error:', error));
}
