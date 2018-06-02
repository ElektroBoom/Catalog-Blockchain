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


@app.route('/carnet', methods=['POST'])
def create_keys():
    carnet.create_keys()
    if carnet.save_keys():
        respone = {
            'public_key': carnet.public_key,
            'private_key': carnet.private_key
        }
        global blockchain
        blockchain = Blockchain(carnet.public_key)
        return jsonify(respone), 201
    else:
        respone = {
            'message': 'Salvarea cheilor a esuat.'
        }
        return jsonify(respone), 500


@app.route('/carnet', methods=['GET'])
def load_keys():
    if carnet.load_keys():
        respone = {
            'public_key': carnet.public_key,
            'private_key': carnet.private_key
        }
        global blockchain
        blockchain = Blockchain(carnet.public_key)
        return jsonify(respone), 201
    else:
        respone = {
            'message': 'Incarcarea cheilor a esuat.'
        }
        return jsonify(respone), 500


@app.route('/mine', methods=['POST'])
def mine():
    block = blockchain.mine_block()
    if block != None:
        dict_block = block.__dict__.copy()
        dict_block['rezultate'] = [
            rez.__dict__ for rez in dict_block['rezultate']]
        reponse = {
            'message': 'Inserarea unui bloc a reusit.',
            'block': dict_block
        }
        return jsonify(reponse), 201
    else:
        reponse = {
            'message': 'Inserarea unui bloc a esuat.',
            'carnet_set_up': carnet.public_key != None
        }
        return jsonify(reponse), 500


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
