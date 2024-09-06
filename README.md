# AI Checkers Game

## Project Overview

This project is an AI-powered Checkers game where two AI players compete against each other. The game uses OpenAI's GPT-3.5-turbo model to determine moves and provides reasoning for each move. It is built using Flask for the backend, JavaScript for the frontend, and SQLAlchemy for database operations.

## Features

- AI-powered gameplay with reasoning for each move.
- A visual board to display the current state of the game.
- The ability to start new games and track game results.
- Utilizes OpenAI API for generating AI moves.
- Simple, elegant, and user-friendly interface.

## Project Structure

The project is organized into the following files:

- **app.py**: The main Flask application file that handles routes and game logic.
- **ai_player.py**: Contains the `AIPlayer` class which interfaces with OpenAI to get moves.
- **game_logic.py**: Contains the `CheckersGame` class which handles game mechanics and rules.
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
- OpenAI API Key (sign up on OpenAI's website)

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

4. **Set up environment variables:**
    ```bash
    export OPENAI_API_KEY=<your-openai-api-key>
    ```

5. **Initialize the database:**
    ```bash
    python -c "from database import init_db; init_db()"
    ```

6. **Run the application:**
    ```bash
    flask run
    ```

### Usage Guide

1. **Start a New Game:**
    - Open your browser and navigate to `http://localhost:5000/`.
    - Click the "Start New Game" button to start a new game.

2. **Gameplay:**
    - The AI players will make moves automatically.
    - The board will update to show the current state of the game.
    - The reasoning for each move will be displayed below the board.

3. **Game Over:**
    - When the game is over, an alert will display the winner.
    - The game result will be saved in the database.

### Technical Details

- **Backend**: Flask serves as the web framework, handling routes and game logic.
- **Frontend**: JavaScript (with Fetch API) handles real-time updates and interactions.
- **Database**: SQLAlchemy is used for ORM and SQLite for storage.
- **AI Integration**: OpenAI's GPT-3.5-turbo model generates the AI moves and provides reasoning.

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