from flask import Flask, render_template, jsonify, request
from game_logic import CheckersGame
from ai_player import AIPlayer
from database import init_db, save_game_result
import config

app = Flask(__name__)
app.config.from_object(config.Config)

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    game = CheckersGame()
    player1 = AIPlayer("Player 1")
    player2 = AIPlayer("Player 2")
    game_id = game.id
    return jsonify({"game_id": game_id, "board": game.get_board()})

@app.route('/make_move', methods=['POST'])
def make_move():
    game_id = request.json['game_id']
    game = CheckersGame.get_game(game_id)
    current_player = AIPlayer("Current Player")
    move, reasoning = current_player.get_move(game)
    game.make_move(move)
    
    if game.is_game_over():
        winner = game.get_winner()
        save_game_result(game_id, winner)
        return jsonify({
            "board": game.get_board(),
            "game_over": True,
            "winner": winner,
            "reasoning": reasoning
        })
    
    return jsonify({
        "board": game.get_board(),
        "game_over": False,
        "reasoning": reasoning
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
