from flask import Flask, request
import find_prices

app = Flask(__name__)


@app.route('/check-prices', methods=['GET'])
def json_game_prices():
    request_data = request.get_json()

    game_name = None

    try:
        if request_data:
            if 'Game Name' in request_data:
                game_name = request_data['Game Name']

        return find_prices.find_game_prices(game_name)

    except IndexError:
        return {"Index Error": "Game name must be a string."}
    except TypeError:
        return {"Type Error": "Game name must be a string."}


if __name__ == '__main__':
    app.run(debug=True, port=5000)
