from flask import Flask, jsonify, request
from flask_cors import CORS

from carnet import Carnet
from blockchain import Blockchain
from info_didactic import InfoDidactic
from types import SimpleNamespace
from json import loads

app = Flask(__name__)
carnet = Carnet()
blockchain = Blockchain(carnet.public_key)
CORS(app)


@app.route('/carnet', methods=['POST'])
def create_keys():
    carnet.create_keys()
    if carnet.save_keys():
        global blockchain
        blockchain = Blockchain(carnet.public_key)
        response = {
            'public_key': carnet.public_key,
            'private_key': carnet.private_key
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Salvarea cheilor a esuat'
        }
        return jsonify(response), 500


@app.route('/carnet', methods=['GET'])
def load_keys():
    if carnet.load_keys():
        global blockchain
        blockchain = Blockchain(carnet.public_key)
        response = {
            'public_key': carnet.public_key,
            'private_key': carnet.private_key
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Incarcarea cheilor a esuat'
        }
        return jsonify(response), 500


@app.route('/', methods=['GET'])
def get_ui():
    return 'Merge'


@app.route('/mine', methods=['POST'])
def mine():
    block = blockchain.mine_block()
    if block != None:
        dict_block = block.__dict__.copy()
        dict_block['rezultate'] = [rez.to_ordered_dict()
                                   for rez in dict_block['rezultate']]
        response = {
            'message': 'Adaugarea unui block a reusit',
            'block': dict_block
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Adaugarea unui block a esuat',
            'carnet_set_up': carnet.public_key != None
        }
        return jsonify(response), 500


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot = blockchain.chain
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    for dict_block in dict_chain:
        dict_block['rezultate'] = [rez.to_ordered_dict()
                                   for rez in dict_block['rezultate']]
    return jsonify(dict_chain), 200


@app.route('/rezultat', methods=['POST'])
def add_rezultat():
    if carnet.public_key == None:
        response = {
            'message': 'Nu am carnet'
        }
        return jsonify(response), 400
    values = request.get_json()
    if not values:
        response = {
            'message': 'Nu am gasit date'
        }
        return jsonify(response), 400
    required_fields = ['receptor', 'info_didactic']
    if not all(field in values for field in required_fields):
        response = {
            'message': 'Nu am toate datele'
        }
        return jsonify(response), 400
    receptor = values['receptor']
    info_didactic_data = values['info_didactic']
    info_didactic = InfoDidactic(info_didactic_data['tip_info'],
                                 info_didactic_data['materie'],
                                 info_didactic_data['descriere'],
                                 info_didactic_data['nota'],
                                 info_didactic_data['an_scolar'],
                                 info_didactic_data['data_intamplarii'],
                                 info_didactic_data['unitate_invatamant'],
                                 info_didactic_data['specializare'],
                                 info_didactic_data['comentariu'])
    semnatura = carnet.sign_rezultat(
        carnet.public_key, receptor, info_didactic)
    if blockchain.add_nota(carnet.public_key, receptor, info_didactic, semnatura):
        response = {
            'message': 'Adaugarea unei note a reusit',
            'rezultat': {
                'emitator': carnet.public_key,
                'receptor': receptor,
                'info_didactic': info_didactic_data,
                'semnatura': semnatura
            }
        }
        return jsonify(response), 500
    else:
        response = {
            'message': 'Adaugarea unei note a esuat'
        }
        return jsonify(response), 500


@app.route('/rezultate', methods=['GET'])
def get_rezultate():
    rezultate = blockchain.get_rezultate()
    if rezultate != None:
        response = {
            'message': 'Returnarea rezultate a reusit',
            'rezultate': [rez.to_ordered_dict() for rez in rezultate]
        }
        return jsonify(response), 200

    else:
        response = {
            'message': 'Retunartea rezultatelor a esuat',
            'carnet_set_up': carnet.public_key != None
        }
        return jsonify(response), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=51328)
