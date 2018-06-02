from flask import Flask, jsonify, request
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
        dict_block = vars(block).copy()
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


@app.route('/add_rezultat', methods=['POST'])
def add_info_didactic():
    if carnet.public_key == None:
        reponse = {
            'message': 'Nu e setat carnetul'
        }
        return jsonify(reponse), 400
    values = request.get_json()
    if not values:
        reponse = {
            'message': 'Nu am date'
        }
        return jsonify(reponse), 400
    required_fields = ['receptor', 'info_didactic']
    if not all(field in values for field in required_fields):
        reponse = {
            'message': 'Lipsesc date'
        }
        return jsonify(reponse), 400
    receptor = values['receptor']
    info_didactic = values['info_didactic']
    signature = carnet.sign(carnet.public_key, receptor, info_didactic)
    succes = blockchain.add_nota(
        carnet.public_key, receptor, info_didactic, signature)
    if succes:
        reponse = {
            'message': 'Adaugarea de nota/absenta a reusit',
            'info_didactic': {
                'emitator': carnet.public_key,
                'receptor': receptor,
                'info_didactic': info_didactic,
                'signature': signature
            }
        }
        return jsonify(reponse), 201
    else:
        reponse = {
            'message': 'Adaugarea de nota/absenta a esuat'
        }
        return jsonify(reponse), 400


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_shanpshot = blockchain.chain
    dict_chain = [block.__dict__.copy() for block in chain_shanpshot]
    for dict_block in dict_chain:
        dict_block['rezultate'] = [
            rez.__dict__ for rez in dict_block['rezultate']]
    return jsonify(dict_chain), 200


@app.route('/rezultate', methods=['GET'])
def get_rezultate():
    rezultate = blockchain.get_rezultate()
    if rezultate != None:
        respone = {
            'message': 'Afisarea rezultatelor a reusit.',
            'rezultate': rezultate
        }
    else:
        respone = {
            'message': 'Afisarea rezultatelor a esuat.',
            'carnet_set_up': carnet.public_key != None
        }
        return jsonify(respone), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=51328)
