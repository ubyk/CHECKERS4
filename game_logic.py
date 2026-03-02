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

    def is_within_bounds(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def belongs_to_current_player(self, piece):
        return piece != ' ' and piece.lower() == self.current_player[0]

    def is_opponent_piece(self, piece):
        return piece != ' ' and piece.lower() != self.current_player[0]

    def get_piece_directions(self, piece):
        if piece.isupper():
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if piece.lower() == 'r':
            return [(1, -1), (1, 1)]
        return [(-1, -1), (-1, 1)]

    def crown_piece(self, piece, row):
        if piece == 'r' and row == 7:
            return 'R'
        if piece == 'b' and row == 0:
            return 'B'
        return piece

    def clone_board(self, board):
        return [board_row[:] for board_row in board]

    def apply_step_to_board(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end
        piece = board[start_row][start_col]

        board[end_row][end_col] = piece
        board[start_row][start_col] = ' '

        if abs(start_row - end_row) == 2:
            jump_row = (start_row + end_row) // 2
            jump_col = (start_col + end_col) // 2
            board[jump_row][jump_col] = ' '

        board[end_row][end_col] = self.crown_piece(board[end_row][end_col], end_row)

    def get_simple_moves_for_piece(self, row, col):
        piece = self.board[row][col]
        if not self.belongs_to_current_player(piece):
            return []

        moves = []
        for dr, dc in self.get_piece_directions(piece):
            end_row = row + dr
            end_col = col + dc
            if self.is_within_bounds(end_row, end_col) and self.board[end_row][end_col] == ' ':
                moves.append([((row, col), (end_row, end_col))])
        return moves

    def get_captures_for_piece(self, row, col, board=None, piece=None):
        if board is None:
            board = self.board
        if piece is None:
            piece = board[row][col]

        captures = []
        found_capture = False

        for dr, dc in self.get_piece_directions(piece):
            mid_row = row + dr
            mid_col = col + dc
            end_row = row + 2 * dr
            end_col = col + 2 * dc

            if not self.is_within_bounds(end_row, end_col):
                continue

            middle_piece = board[mid_row][mid_col]
            if middle_piece == ' ' or middle_piece.lower() == self.current_player[0]:
                continue
            if board[end_row][end_col] != ' ':
                continue

            found_capture = True
            next_board = self.clone_board(board)
            start = (row, col)
            end = (end_row, end_col)
            self.apply_step_to_board(next_board, start, end)
            moved_piece = next_board[end_row][end_col]
            continuation = self.get_captures_for_piece(end_row, end_col, next_board, moved_piece)

            if continuation:
                for follow_up in continuation:
                    captures.append([(start, end)] + follow_up)
            else:
                captures.append([(start, end)])

        if found_capture:
            return captures
        return []

    def get_all_valid_moves(self):
        capture_moves = []
        simple_moves = []

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if not self.belongs_to_current_player(piece):
                    continue
                capture_moves.extend(self.get_captures_for_piece(row, col))
                if not capture_moves:
                    simple_moves.extend(self.get_simple_moves_for_piece(row, col))

        if capture_moves:
            return capture_moves
        return simple_moves

    def normalize_move(self, move):
        if isinstance(move, tuple):
            if len(move) == 2 and all(isinstance(pos, tuple) and len(pos) == 2 for pos in move):
                return [move]
        if isinstance(move, list) and move:
            if all(
                isinstance(step, tuple) and len(step) == 2 and
                all(isinstance(pos, tuple) and len(pos) == 2 for pos in step)
                for step in move
            ):
                return move
        raise ValueError("Invalid move format")

    def is_valid_move(self, start, end):
        return [((start[0], start[1]), (end[0], end[1]))] in self.get_all_valid_moves()

    def make_move(self, move):
        normalized_move = self.normalize_move(move)
        if normalized_move not in self.get_all_valid_moves():
            raise ValueError("Invalid move")

        for start, end in normalized_move:
            self.apply_step_to_board(self.board, start, end)

        self.current_player = 'black' if self.current_player == 'red' else 'red'

    def is_game_over(self):
        red_pieces = sum(row.count('r') + row.count('R') for row in self.board)
        black_pieces = sum(row.count('b') + row.count('B') for row in self.board)
        return red_pieces == 0 or black_pieces == 0 or not self.has_valid_moves()

    def has_valid_moves(self):
        return bool(self.get_all_valid_moves())

    def get_winner(self):
        if not self.is_game_over():
            return None

        red_pieces = sum(row.count('r') + row.count('R') for row in self.board)
        black_pieces = sum(row.count('b') + row.count('B') for row in self.board)
        if red_pieces == 0:
            return 'black'
        if black_pieces == 0:
            return 'red'
        if not self.has_valid_moves():
            return 'black' if self.current_player == 'red' else 'red'
        return 'draw'

    @staticmethod
    def get_game(game_id):
        # In a real implementation, this would fetch the game from a database or cache
        # For simplicity, we're creating a new game each time
        return CheckersGame()
