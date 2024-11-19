// static/app.js

const appDiv = document.getElementById("gameContent");

// Helper function to send POST requests
const postRequest = async (endpoint, data = {}) => {
  const response = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return response.json();
};

// Start game
document.getElementById("startButton").addEventListener("click", async () => {
  const response = await postRequest("/start");
  appDiv.innerHTML = `<p>${response.message}</p>`;
  showNextStepButton();
});

// Next step in the game
const showNextStepButton = () => {
  const nextButton = document.createElement("button");
  nextButton.textContent = "Next Step";
  nextButton.addEventListener("click", async () => {
    const response = await postRequest("/next");
    appDiv.innerHTML += `<p>${response.message}</p>`;
    showChoiceButton();
  });
  appDiv.appendChild(nextButton);
};

// Make a choice
const showChoiceButton = () => {
  const choiceButton = document.createElement("button");
  choiceButton.textContent = "Make a Choice";
  choiceButton.addEventListener("click", async () => {
    const userChoice = Math.floor(Math.random() * 3) + 1; // Random choice for demo
    const response = await postRequest("/choice", { choice: userChoice });
    appDiv.innerHTML += `<p>${response.message}</p>`;
  });
  appDiv.appendChild(choiceButton);
};