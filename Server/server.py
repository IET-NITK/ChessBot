from flask import Flask, request, jsonify
import utils

app = Flask(__name__)

@app.route('/start_game')
def start():

    utils.new_game()

    response = jsonify({
        'msg': "New Game Started!"
    })

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/get_move')
def get_move():

    response = jsonify({
        'move': utils.get_best_move()
    })

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/push_move', methods = ['POST'])
def push_move():

    move = request.form['move']

    utils.push_move_to_board(move)

    response = jsonify({
        'msg': "Move pushed to board"
    })

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == '__main__':
    print('Server started successfully at port 5000...')
    utils.load_assets()
    app.run()