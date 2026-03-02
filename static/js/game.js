let gameId = null;
let currentBoard = null;
let currentPlayer = null;
let gameInProgress = false;

document.getElementById('startNewGame').addEventListener('click', startNewGame);
document.getElementById('resetGame').addEventListener('click', resetGame);

function startNewGame() {
    fetch('/start_game', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            gameId = data.game_id;
            currentBoard = data.board;
            currentPlayer = data.current_player;
            renderBoard();
            gameInProgress = true;
            const startButton = document.getElementById('startNewGame');
            if (startButton) startButton.disabled = true;
            const reasoningElement = document.getElementById('reasoning');
            if (reasoningElement) {
                reasoningElement.textContent = 'Game started. Red moves first.';
            }
            makeMove();
        });
}

function resetGame() {
    fetch('/start_game', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            gameId = data.game_id;
            currentBoard = data.board;
            currentPlayer = data.current_player;
            renderBoard();
            const reasoningElement = document.getElementById('reasoning');
            if (reasoningElement) {
                reasoningElement.textContent = 'Game reset. Starting a fresh AI vs AI match.';
            }
            const startButton = document.getElementById('startNewGame');
            if (startButton) startButton.disabled = false;
            gameInProgress = false;
        });
}

function renderBoard() {
    const boardElement = document.getElementById('board');
    if (!boardElement) return;

    boardElement.innerHTML = '';

    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const cell = document.createElement('div');
            cell.className = `cell ${(row + col) % 2 === 0 ? 'light' : 'dark'}`;

            if (currentBoard[row][col] !== ' ') {
                const piece = document.createElement('div');
                piece.className = `piece ${currentBoard[row][col].toLowerCase() === 'r' ? 'red' : 'black'}`;
                if (currentBoard[row][col].toUpperCase() === currentBoard[row][col]) {
                    piece.classList.add('king');
                }
                cell.appendChild(piece);
            }

            boardElement.appendChild(cell);
        }
    }

    const currentPlayerElement = document.getElementById('current-player');
    if (currentPlayerElement) {
        currentPlayerElement.textContent = `Current player: ${currentPlayer.toUpperCase()}`;
    }
}

function makeMove() {
    if (!gameInProgress) return;

    fetch('/make_move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ game_id: gameId }),
    })
    .then(response => response.json())
    .then(data => {
        currentBoard = data.board;
        currentPlayer = data.current_player;
        renderBoard();
        const reasoningElement = document.getElementById('reasoning');
        if (reasoningElement) {
            reasoningElement.textContent = `${data.last_player.toUpperCase()} move: ${data.reasoning}`;
        }

        if (data.game_over) {
            alert(`Game Over! Winner: ${data.winner}`);
            const startButton = document.getElementById('startNewGame');
            if (startButton) startButton.disabled = false;
            gameInProgress = false;
        } else {
            setTimeout(makeMove, 2000);
        }
    });
}
