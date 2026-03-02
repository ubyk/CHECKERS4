import random

class AIPlayer:
    def __init__(self, name):
        self.name = name

    def get_move(self, game):
        valid_moves = self.get_valid_moves(game)
        if not valid_moves:
            return None, "No valid moves available."

        move = self.choose_best_move(game, valid_moves)
        reasoning = self.describe_move(move)
        return move, reasoning

    def get_valid_moves(self, game):
        return game.get_all_valid_moves()

    def choose_best_move(self, game, valid_moves):
        captures = [
            move for move in valid_moves
            if any(abs(start[0] - end[0]) == 2 for start, end in move)
        ]
        if captures:
            longest_capture = max(len(move) for move in captures)
            strongest_captures = [move for move in captures if len(move) == longest_capture]
            return random.choice(strongest_captures)
        return random.choice(valid_moves)

    def describe_move(self, move):
        path = [move[0][0]] + [step[1] for step in move]
        path_text = " -> ".join(str(position) for position in path)
        if any(abs(start[0] - end[0]) == 2 for start, end in move):
            return f"Capture sequence: {path_text}"
        return f"Move chosen: {path_text}"
