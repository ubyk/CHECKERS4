let gameId = null;
let currentBoard = null;

function startGame() {
    fetch('/start_game', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            gameId = data.game_id;
            currentBoard = data.board;
            renderBoard();
            document.getElementById('start-button').disabled = true;
            makeMove();
        });
}

function makeMove() {
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
            renderBoard();
            document.getElementById('reasoning').textContent = data.reasoning;

            if (data.game_over) {
                alert(`Game Over! Winner: ${data.winner}`);
                document.getElementById('start-button').disabled = false;
            } else {
                setTimeout(makeMove, 2000);  // Wait 2 seconds before the next move
            }
        });
}

function renderBoard() {
    const boardElement = document.getElementById('board');
    boardElement.innerHTML = '';

    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const cell = document.createElement('div');
            cell.className = `cell ${(row + col) % 2 === 0 ? 'light' : 'dark'}`;

            if (currentBoard[row][col] !== ' ') {
                const piece = document.createElement('div');
                piece.className = `piece ${currentBoard[row][col].toLowerCase() === 'r' ? 'red' : 'black'}`;
                cell.appendChild(piece);
            }

            boardElement.appendChild(cell);
        }
    }
}

document.getElementById('start-button').addEventListener('click', startGame);
