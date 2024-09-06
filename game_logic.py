import uuid

class CheckersGame:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.board = self.create_initial_board()
        self.current_player = 'red'

    def create_initial_board(self):
        board = [[' ' for _ in range(8)] for _ in range(8)]
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'r'
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'b'
        return board

    def get_board(self):
        return self.board

    def is_valid_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end

        # Check if the move is within the board
        if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
            return False

        # Check if the start position contains the current player's piece
        if self.board[start_row][start_col].lower() != self.current_player[0]:
            return False

        # Check if the end position is empty
        if self.board[end_row][end_col] != ' ':
            return False

        # Check if the move is diagonal
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False

        # Check if the move is forward (unless it's a king)
        if self.board[start_row][start_col].islower():
            if (self.current_player == 'red' and end_row <= start_row) or \
               (self.current_player == 'black' and end_row >= start_row):
                return False

        # Check if it's a valid single move or jump
        if abs(start_row - end_row) == 1:
            return True
        elif abs(start_row - end_row) == 2:
            jump_row = (start_row + end_row) // 2
            jump_col = (start_col + end_col) // 2
            return self.board[jump_row][jump_col].lower() != self.current_player[0] and \
                   self.board[jump_row][jump_col] != ' '

        return False

    def make_move(self, move):
        start, end = move
        if self.is_valid_move(start, end):
            start_row, start_col = start
            end_row, end_col = end

            # Move the piece
            self.board[end_row][end_col] = self.board[start_row][start_col]
            self.board[start_row][start_col] = ' '

            # Check if it's a jump and remove the jumped piece
            if abs(start_row - end_row) == 2:
                jump_row = (start_row + end_row) // 2
                jump_col = (start_col + end_col) // 2
                self.board[jump_row][jump_col] = ' '

            # Check if the piece should be kinged
            if (self.current_player == 'red' and end_row == 7) or \
               (self.current_player == 'black' and end_row == 0):
                self.board[end_row][end_col] = self.board[end_row][end_col].upper()

            # Switch players
            self.current_player = 'black' if self.current_player == 'red' else 'red'
        else:
            raise ValueError("Invalid move")

    def is_game_over(self):
        red_pieces = sum(row.count('r') + row.count('R') for row in self.board)
        black_pieces = sum(row.count('b') + row.count('B') for row in self.board)
        return red_pieces == 0 or black_pieces == 0 or not self.has_valid_moves()

    def has_valid_moves(self):
        for row in range(8):
            for col in range(8):
                if self.board[row][col].lower() == self.current_player[0]:
                    for dr in [-1, 1]:
                        for dc in [-1, 1]:
                            if self.is_valid_move((row, col), (row + dr, col + dc)) or \
                               self.is_valid_move((row, col), (row + 2*dr, col + 2*dc)):
                                return True
        return False

    def get_winner(self):
        if not self.is_game_over():
            return None
        red_pieces = sum(row.count('r') + row.count('R') for row in self.board)
        black_pieces = sum(row.count('b') + row.count('B') for row in self.board)
        if red_pieces > black_pieces:
            return 'red'
        elif black_pieces > red_pieces:
            return 'black'
        else:
            return 'draw'

    @staticmethod
    def get_game(game_id):
        # In a real implementation, this would fetch the game from a database or cache
        # For simplicity, we're creating a new game each time
        return CheckersGame()