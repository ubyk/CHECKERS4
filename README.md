# AI vs AI Checkers

## Project Overview

This project is a web-based Checkers prototype where two automated players compete against each other. It uses Flask for the backend, JavaScript for the frontend, and SQLAlchemy with SQLite for storing completed game results.

## Features

- AI vs AI gameplay in the browser.
- A visual board that updates after every turn.
- Basic move narration for each AI turn.
- SQLite persistence for completed match results.
- Checkers rules with forced captures, multi-captures, and kings.

## Project Structure

The project is organized into the following files:

- **app.py**: The main Flask application file that handles routes and game logic.
- **ai_player.py**: Contains the `AIPlayer` class and move-selection logic.
- **game_logic.py**: Contains the `CheckersGame` class and the checkers rules engine.
- **database.py**: Manages database connections and defines the `GameResult` model.
- **config.py**: Configuration file for the Flask application.
- **templates/**: Contains HTML templates for rendering web pages.
  - **index.html**: The main game interface.
- **static/**: Contains static assets like CSS and JavaScript files.
  - **css/style.css**: Stylesheet for the game interface.
  - **js/game.js**: JavaScript file handling the game logic on the frontend.
- **requirements.txt**: Lists the Python dependencies required to run the project.

## Setup Instructions

### Prerequisites

- Python 3.7+

### Installation

1. **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate # For Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Initialize the database:**
    ```bash
    python -c "from database import init_db; init_db()"
    ```

5. **Run the application:**
    ```bash
    flask run
    ```

### Usage Guide

1. **Start a New Match:**
    - Open your browser and navigate to `http://localhost:5000/`.
    - Click the "Start Match" button to begin an automated game.

2. **Gameplay:**
    - The AI players will make moves automatically every few seconds.
    - The board will update to show the current state of the game.
    - The move summary for each turn will be displayed below the board.

3. **Game Over:**
    - When the game is over, an alert will display the winner.
    - The game result will be saved in the database.

### Technical Details

- **Backend**: Flask serves as the web framework, handling routes and game logic.
- **Frontend**: JavaScript (with Fetch API) handles real-time updates and interactions.
- **Database**: SQLAlchemy is used for ORM and SQLite for storage.
- **Move Selection**: The AI currently selects from legal moves, prioritizing the longest available capture sequences.

### Current Scope and Limitations

- The project is currently `AI vs AI` only; there is no player-vs-AI mode.
- The AI is rule-based and does not use an OpenAI model.
- Kings move one square diagonally at a time and capture by jumping, not as flying kings.
- Draw detection is limited; repetition-based or long-endgame draw rules are not implemented.

### Contribution Guide

1. **Fork the repository:**
    Click the "Fork" button on the repository's GitHub page.

2. **Clone your fork:**
    ```bash
    git clone <your-fork-url>
    cd <repository-directory>
    ```

3. **Create a new branch:**
    ```bash
    git checkout -b <branch-name>
    ```

4. **Make your changes and commit them:**
    ```bash
    git commit -am "Add some feature"
    ```

5. **Push to the branch:**
    ```bash
    git push origin <branch-name>
    ```

6. **Create a new Pull Request:**
    Open a pull request on GitHub and provide a description of your changes.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
