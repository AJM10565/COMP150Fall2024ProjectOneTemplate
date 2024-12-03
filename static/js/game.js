const postRequest = async (endpoint, data = {}) => {
    const response = await fetch(`http://127.0.0.1:5000${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    return response.json();
};

const displayRiddle = (riddleQuestion, riddleOptions) => {
    const riddleContainer = document.getElementById("riddle-container");
    const riddleElement = document.getElementById("riddle");
    const optionsElement = document.getElementById("options");

    riddleElement.textContent = riddleQuestion;
    optionsElement.innerHTML = "";
    riddleOptions.forEach((option, index) => {
        const button = document.createElement("button");
        button.textContent = option;
        button.onclick = () => makeChoice(index);
        optionsElement.appendChild(button);
    });

    riddleContainer.style.display = "block";
};

const startGame = async () => {
    const response = await postRequest("/start");
    displayRiddle(response.riddle_question, response.riddle_options);
};

const nextStep = async () => {
    const response = await postRequest("/next");
    displayRiddle(response.riddle_question, response.riddle_options);
};

const makeChoice = async (choice) => {
    const response = await postRequest("/choice", { choice: choice });
    if (response.message.includes("riddle")) {
        displayRiddle(response.riddle_question, response.riddle_options);
    } else {
        updateOutput(response.message);
    }
};
