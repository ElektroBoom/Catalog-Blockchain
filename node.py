from flask import Flask
from flask_cors import CORS
from carnet import Carnet

app = Flask(__name__)
carnet = Carnet()
CORS(app)


@app.route('/', methods=['GET'])
def get_ui():
    return 'Merge'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=51328)
