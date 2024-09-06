let gameId = null;
let currentBoard = null;
let currentPlayer = null;
let gameInProgress = false;
let selectedPiece = null;

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
            document.getElementById('reasoning').textContent = '';
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
            cell.id = `square-${row}-${col}`;
            cell.onclick = () => handlePieceSelection(row, col);

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
            reasoningElement.textContent = `${data.current_player.toUpperCase()} player's move: ${data.reasoning}`;
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

function handlePieceSelection(row, col) {
    if (!gameInProgress) return;

    if (selectedPiece) {
        const move = [selectedPiece.row, selectedPiece.col, row, col];
        if (isValidMove(move)) {
            makePlayerMove(move);
            selectedPiece = null;
            clearHighlights();
        } else {
            selectedPiece = null;
            clearHighlights();
            handlePieceSelection(row, col);
        }
    } else {
        if (currentBoard[row][col].toLowerCase() === currentPlayer[0]) {
            selectedPiece = { row, col };
            highlightMoves(getValidMoves(row, col));
        }
    }
}

function highlightMoves(validMoves) {
    validMoves.forEach(move => {
        const square = document.getElementById(`square-${move[2]}-${move[3]}`);
        if (square) {
            square.classList.add('highlight-valid');
        }
    });
}

function clearHighlights() {
    const highlightedSquares = document.querySelectorAll('.highlight-valid');
    highlightedSquares.forEach(square => {
        square.classList.remove('highlight-valid');
    });
}

function getValidMoves(row, col) {
    // This is a simplified version. You should implement the actual game rules here.
    const validMoves = [];
    const directions = (currentPlayer === 'red') ? [[1, -1], [1, 1]] : [[-1, -1], [-1, 1]];

    directions.forEach(([dr, dc]) => {
        if (isValidSquare(row + dr, col + dc) && currentBoard[row + dr][col + dc] === ' ') {
            validMoves.push([row, col, row + dr, col + dc]);
        }
        if (isValidSquare(row + 2*dr, col + 2*dc) && 
            currentBoard[row + dr][col + dc].toLowerCase() !== currentPlayer[0] &&
            currentBoard[row + dr][col + dc] !== ' ' &&
            currentBoard[row + 2*dr][col + 2*dc] === ' ') {
            validMoves.push([row, col, row + 2*dr, col + 2*dc]);
        }
    });

    return validMoves;
}

function isValidSquare(row, col) {
    return row >= 0 && row < 8 && col >= 0 && col < 8;
}

function isValidMove(move) {
    const validMoves = getValidMoves(move[0], move[1]);
    return validMoves.some(validMove => 
        validMove[0] === move[0] && 
        validMove[1] === move[1] && 
        validMove[2] === move[2] && 
        validMove[3] === move[3]
    );
}

function makePlayerMove(move) {
    fetch('/make_player_move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ game_id: gameId, move: move }),
    })
    .then(response => response.json())
    .then(data => {
        currentBoard = data.board;
        currentPlayer = data.current_player;
        renderBoard();
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