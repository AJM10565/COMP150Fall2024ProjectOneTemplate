# COMP150 Fall 2024 Project 

This is Kaelen Bober and Max Uribe's Comp150 Fall 2024 Poject. We have created a Star Wars adventure game, where you choose members of the Star Wars universe to join your party and take down an Imperial Star Destroyer, becoming honorable (digital) heros! 

## How to Run the Project

To run our fancy text based Star Wars adventure game, follow the steps below:

### Prerequisites
- Python 3.12.6 installed on your machine.

### Steps to Run

1. Clone or download the project to your local machine.

2. Navigate to the project root directory (assumed to be named `comp150fall2024projectonetemplate`):

   ```bash
   cd comp150fall2024projectonetemplate
   ```

3. Run the game using Python:

   ```bash
   python project_code/src/main.py
   ```

### Game Flow

- The game will prompt you with an intro message, explaining the story of our game, your choice of heros, what to expect in each stage of the game. 
Press enter and you're then prompted to choose three characters, then you're thrown into the first event of the game.
- Follow the instructions displayed in the terminal to play through the game.

### Example

After running the game, going through the intro and choosing your characters, you will see a series of prompts like:

```
+----------------------------------------------------+
|                 Docking Area                       |
+----------------------------------------------------+
| You've reached the hidden docking bay. Do you      |
| prepare your ship for a quick getaway or try to    |
| sabotage the Imperial crafts?                      |
+----------------------------------------------------+

Choose a party member:
1. Obi-wan
2. Han Solo
3. R2-D2

Enter the number of the chosen party member: 
```

Simply follow the prompts to make your choices to see the outcomes.

### Running Unit Tests

To run the provided unit tests, we recommend using `pytest`, a testing framework for Python.

#### Steps to Run Tests:

1. First, make sure `pytest` is installed on your machine:

   ```bash
   pip install pytest
   ```

2. Run the tests by navigating to the project root and executing the following command:

   ```bash
   pytest
   ```

This will discover and run all the tests in the `test/` directory.

### Example Test Output:

After running the tests, you should see output like this:

```
============================= test session starts ==============================
collected 3 items

test/test_game.py ...                                                     [100%]

============================== 3 passed in 0.05s ===============================
```

### Project Structure

Here is the project directory structure:

```
.
├── PROJECT_INSTRUCTIONS.md
├── README.md
├── __init__.py
└── project_code
    ├── __init__.py
    ├── location_events
    │   ├── jedha_events.json
    │   └── star_destroyer_events.json
    ├── src
    │   ├── display_winning_crawl.py
    │   ├── main.py
    │   ├── opening_crawl.py
    │   └── star_destroyer_prompt.py
    └── test
        ├── __init__.py
        └── test_game.py
```

- `project_code/` - The main directory containing all the code for the project.
    - `location_events/` - Directory containing the JSON files with events for the game.
    - `src/` - Source code for the project.
    - `test/` - Directory for tests to ensure the game functions correctly.
- `README.md` - This file, with instructions on how to run the project.
- `PROJECT_INSTRUCTIONS.md` - Additional instructions or guidelines for the project.

---

Enjoy your adventure!

