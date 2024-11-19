  document.addEventListener("DOMContentLoaded", () => {
    // Create and apply styles dynamically
    const style = document.createElement("style");
    style.innerHTML = `
      body {
        font-family: Arial, sans-serif;
        background-color: #f0f8ff;
        text-align: center;
        padding: 20px;
      }
      h1 {
        color: #2c3e50;
      }
      button {
        padding: 10px 20px;
        margin: 10px;
        font-size: 16px;
        background-color: #3498db;
        color: white;
        border: none;
        cursor: pointer;
      }
      button:hover {
        background-color: #2980b9;
      }
      #output {
        margin-top: 20px;
        padding: 20px;
        background: #ecf0f1;
        border-radius: 8px;
        font-family: monospace;
        text-align: left;
        overflow-y: auto;
        max-height: 400px;
      }
    `;
    document.head.appendChild(style);

    // Create main container
    const body = document.body;

    const title = document.createElement("h1");
    title.textContent = "🌟 Welcome to Bikini Bottom Adventure! 🌟";
    body.appendChild(title);

    const gameContainer = document.createElement("div");
    gameContainer.id = "game-container";
    const instructions = document.createElement("p");
    instructions.textContent = "Start your adventure and make your choices!";
    gameContainer.appendChild(instructions);

    // Create buttons
    const buttons = [
      { text: "Start Game", onClick: startGame },
      { text: "Next Step", onClick: nextStep },
      { text: "Choice 1", onClick: () => makeChoice(1) },
      { text: "Choice 2", onClick: () => makeChoice(2) },
      { text: "Choice 3", onClick: () => makeChoice(3) },
    ];

    buttons.forEach(({ text, onClick }) => {
      const button = document.createElement("button");
      button.textContent = text;
      button.onclick = onClick;
      gameContainer.appendChild(button);
    });

    body.appendChild(gameContainer);

    // Create output section
    const output = document.createElement("div");
    output.id = "output";
    output.textContent = "Game output will appear here.";
    body.appendChild(output);

    // Game logic functions
    async function startGame() {
      updateOutput("Loading...");
      try {
        const response = await fetch("/start", { method: "POST" });
        const data = await response.json();
        updateOutput(data.message);
      } catch (error) {
        updateOutput("Error: Unable to start the game!");
      }
    }

    async function nextStep() {
      updateOutput("Loading...");
      try {
        const response = await fetch("/next", { method: "POST" });
        const data = await response.json();
        updateOutput(data.message);
      } catch (error) {
        updateOutput("Error: Unable to proceed to the next step!");
      }
    }

    async function makeChoice(choice) {
      updateOutput("Loading...");
      try {
        const response = await fetch("/choice", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ choice }),
        });
        const data = await response.json();
        updateOutput(data.message);
      } catch (error) {
        updateOutput("Error: Unable to process your choice!");
      }
    }

    // Helper function to update the output section
    function updateOutput(message) {
      output.textContent = message;
    }
  });
