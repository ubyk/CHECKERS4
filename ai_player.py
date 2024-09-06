import openai
import os
import random
import re

class AIPlayer:
    def __init__(self, name):
        self.name = name
        openai.api_key = os.environ.get('OPENAI_API_KEY')

    def get_move(self, game):
        valid_moves = self.get_valid_moves(game)
        if not valid_moves:
            return None, "No valid moves available."

        prompt = self.create_prompt(game, valid_moves)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150
            )
            move_text = response.choices[0].message['content']
            move, reasoning = self.parse_response(move_text, valid_moves)
        except Exception as e:
            print(f"Error in AI response: {e}")
            move = random.choice(valid_moves)
            reasoning = f"Random move due to AI error: {str(e)}"

        return move, reasoning

    def get_valid_moves(self, game):
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if game.board[row][col].lower() == game.current_player[0]:
                    for dr in [-1, 1]:
                        for dc in [-1, 1]:
                            if game.is_valid_move((row, col), (row + dr, col + dc)):
                                valid_moves.append(((row, col), (row + dr, col + dc)))
                            if game.is_valid_move((row, col), (row + 2*dr, col + 2*dc)):
                                valid_moves.append(((row, col), (row + 2*dr, col + 2*dc)))
        return valid_moves

    def create_prompt(self, game, valid_moves):
        board_state = '\n'.join([' '.join(row) for row in game.board])
        moves_str = ', '.join([f"({start[0]},{start[1]}) to ({end[0]},{end[1]})" for start, end in valid_moves])
        return f"""
        You are playing a game of checkers. The current board state is:

        {board_state}

        You are the {game.current_player} player. Your valid moves are: {moves_str}
        What is your next move? Provide your move in the format: '(start_row,start_col) to (end_row,end_col)'
        Also, explain your reasoning for this move.
        """

    def parse_response(self, response, valid_moves):
        # Use regex to find the move in various formats
        move_patterns = [
            r'\((\d+)\s*,\s*(\d+)\)\s*to\s*\((\d+)\s*,\s*(\d+)\)',  # (x,y) to (a,b)
            r'(\d+)\s*,\s*(\d+)\s*to\s*(\d+)\s*,\s*(\d+)',          # x,y to a,b
            r'move\s*(\d+)\s*,\s*(\d+)\s*to\s*(\d+)\s*,\s*(\d+)',   # move x,y to a,b
        ]

        for pattern in move_patterns:
            move_match = re.search(pattern, response, re.IGNORECASE)
            if move_match:
                start = (int(move_match.group(1)), int(move_match.group(2)))
                end = (int(move_match.group(3)), int(move_match.group(4)))
                move = (start, end)

                if move in valid_moves:
                    # Extract reasoning (everything after the move)
                    reasoning = response[move_match.end():].strip()
                    return move, reasoning
                else:
                    print(f"Parsed move {move} is not in valid moves: {valid_moves}")
                    break  # Move to fallback logic

        # If we couldn't parse the move or it's invalid, try to extract coordinates
        coord_pattern = r'\b(\d+)\s*,\s*(\d+)\b'
        coords = re.findall(coord_pattern, response)
        
        if len(coords) >= 2:
            start = tuple(map(int, coords[0]))
            end = tuple(map(int, coords[1]))
            move = (start, end)
            
            if move in valid_moves:
                reasoning = f"Move extracted from coordinates. Original response: {response}"
                return move, reasoning

        # If all else fails, choose a random move
        random_move = random.choice(valid_moves)
        return random_move, f"Random move chosen due to parsing error. Original response: {response}"
