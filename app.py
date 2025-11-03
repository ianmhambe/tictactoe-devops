from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Game state
games = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/new-game', methods=['POST'])
def new_game():
    game_id = str(random.randint(1000, 9999))
    games[game_id] = {
        'board': [''] * 9,
        'current_player': 'X',
        'winner': None,
        'game_over': False
    }
    return jsonify({'game_id': game_id, 'game': games[game_id]})

@app.route('/api/move', methods=['POST'])
def make_move():
    data = request.json
    game_id = data.get('game_id')
    position = data.get('position')
    
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    game = games[game_id]
    
    if game['game_over']:
        return jsonify({'error': 'Game is over'}), 400
    
    if game['board'][position] != '':
        return jsonify({'error': 'Position already taken'}), 400
    
    # Make move
    game['board'][position] = game['current_player']
    
    # Check for winner
    winner = check_winner(game['board'])
    if winner:
        game['winner'] = winner
        game['game_over'] = True
    elif '' not in game['board']:
        game['winner'] = 'Draw'
        game['game_over'] = True
    else:
        # Switch player
        game['current_player'] = 'O' if game['current_player'] == 'X' else 'X'
    
    return jsonify({'game': game})

def check_winner(board):
    # Winning combinations
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    
    for combo in wins:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != '':
            return board[combo[0]]
    return None

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
