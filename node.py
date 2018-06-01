from flask import Flask, jsonify
from flask_cors import CORS
from carnet import Carnet
from blockchain import Blockchain

app = Flask(__name__)
carnet = Carnet()
blockchain = Blockchain(carnet.public_key)
CORS(app)


@app.route('/', methods=['GET'])
def get_ui():
    return 'merge'


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_shanpshot = blockchain.chain
    dict_chain = [block.__dict__.copy() for block in chain_shanpshot]
    for dict_block in dict_chain:
        dict_block['rezultate'] = [
            rez.__dict__ for rez in dict_block['rezultate']]
    return jsonify(dict_chain), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=51328)
