import openai
import os
import random

class AIPlayer:
    def __init__(self, name):
        self.name = name
        openai.api_key = os.environ.get('OPENAI_API_KEY')

    def get_move(self, game):
        valid_moves = self.get_valid_moves(game)
        if not valid_moves:
            return None, "No valid moves available."

        # For now, let's use a simple strategy instead of OpenAI
        move = self.choose_best_move(game, valid_moves)
        reasoning = f"Move chosen: {move[0]} to {move[1]}"
        return move, reasoning

    def get_valid_moves(self, game):
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if game.board[row][col].lower() == game.current_player[0]:
                    for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        if game.is_valid_move((row, col), (row + dr, col + dc)):
                            valid_moves.append(((row, col), (row + dr, col + dc)))
                        if game.is_valid_move((row, col), (row + 2*dr, col + 2*dc)):
                            valid_moves.append(((row, col), (row + 2*dr, col + 2*dc)))
        return valid_moves

    def choose_best_move(self, game, valid_moves):
        # Prioritize captures
        captures = [move for move in valid_moves if abs(move[0][0] - move[1][0]) == 2]
        if captures:
            return random.choice(captures)
        return random.choice(valid_moves)