from flask import Flask, render_template, jsonify, request
from game_logic import CheckersGame
from ai_player import AIPlayer
from database import init_db, save_game_result
import config

app = Flask(__name__)
app.config.from_object(config.Config)

init_db()

# Store active games in memory (in a real app, use a database)
active_games = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    game = CheckersGame()
    active_games[game.id] = game
    return jsonify({"game_id": game.id, "board": game.get_board(), "current_player": game.current_player})

@app.route('/make_move', methods=['POST'])
def make_move():
    game_id = request.json['game_id']
    game = active_games.get(game_id)

    if not game:
        return jsonify({"error": "Game not found"}), 404

    current_player = AIPlayer(f"AI {game.current_player.capitalize()}")
    move, reasoning = current_player.get_move(game)

    if move:
        game.make_move(move)

    if game.is_game_over():
        winner = game.get_winner()
        save_game_result(game_id, winner)
        del active_games[game_id]
        return jsonify({
            "board": game.get_board(),
            "game_over": True,
            "winner": winner,
            "reasoning": reasoning,
            "current_player": game.current_player
        })

    return jsonify({
        "board": game.get_board(),
        "game_over": False,
        "reasoning": reasoning,
        "current_player": game.current_player
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)