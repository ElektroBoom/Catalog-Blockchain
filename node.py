from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from carnet import Carnet
from blockchain import Blockchain
from info_didactic import InfoDidactic
from argparse import ArgumentParser

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def get_ui():
    return send_from_directory('ui', 'index.html')


@app.route('/carnet', methods=['POST'])
def create_keys():
    carnet.create_keys()
    if carnet.save_keys():
        global blockchain
        blockchain = Blockchain(carnet.public_key, port)
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
        blockchain = Blockchain(carnet.public_key, port)
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


@app.route('/mine', methods=['POST'])
def mine():
    if blockchain.resolve_conflicts == True:
        response = {
            'message': 'Conflicte in retea. Blocul nu a fost adaugat'
        }
        return jsonify(response), 409
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


@app.route('/resolve_conflicts', methods=['POST'])
def resolve_conflicts():
    replaced = blockchain.resolve()
    if replaced:
        response = {
            'message': 'BLockchain inlocuit'
        }
    else:
        response = {
            'message': 'BLockchain pastrat'
        }
    return jsonify(response), 200


@app.route('/rezultate', methods=['GET'])
def get_rezultate():
    rezultate = blockchain.get_date_de_introdus()
    dict_rezultate = [rez.to_ordered_dict() for rez in rezultate]
    return jsonify(dict_rezultate), 200


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot = blockchain.chain
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    for dict_block in dict_chain:
        dict_block['rezultate'] = [rez.to_ordered_dict()
                                   for rez in dict_block['rezultate']]
    return jsonify(dict_chain), 200


@app.route('/broadcast_note', methods=['POST'])
def broadcast_note():
    values = request.get_json()
    if not values:
        response = {
            'message': 'Nu am gasit date'
        }
        return jsonify(response), 400
    required = ['emitator', 'receptor', 'info_didactic', 'semnatura']
    if not all(key in values for key in required):
        response = {
            'message': 'Lipsesc date'
        }
        return jsonify(response), 400
    emitator = values['emitator']
    receptor = values['receptor']
    info_didactic_data = values['info_didactic']
    info_didactic = InfoDidactic(info_didactic_data['tip_info'],
                                 info_didactic_data['materie'],
                                 info_didactic_data['descriere'],
                                 info_didactic_data['nota'],
                                 info_didactic_data['credite'],
                                 info_didactic_data['an_scolar'],
                                 info_didactic_data['semestru'],
                                 info_didactic_data['data_intamplarii'],
                                 info_didactic_data['tip_unitate'],
                                 info_didactic_data['unitate_invatamant'],
                                 info_didactic_data['specializare'],
                                 info_didactic_data['comentariu'])
    semnatura = values['semnatura']
    if blockchain.add_nota(emitator, receptor, info_didactic, semnatura, is_receiving=True):
        response = {
            'message': 'Adaugarea unei note a reusit',
            'rezultat': {
                'emitator': emitator,
                'receptor': receptor,
                'info_didactic': info_didactic_data,
                'semnatura': semnatura
            }
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'Adaugarea unei note a esuat'
        }
        return jsonify(response), 500


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
                                 info_didactic_data['credite'],
                                 info_didactic_data['an_scolar'],
                                 info_didactic_data['semestru'],
                                 info_didactic_data['data_intamplarii'],
                                 info_didactic_data['tip_unitate'],
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
                'info_didactic': info_didactic.to_ordered_dict(),
                'semnatura': semnatura
            }
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Adaugarea unei note a esuat reeee'
        }
        return jsonify(response), 500


@app.route('/broadcast_block', methods=['POST'])
def broadcast_block():
    values = request.get_json()
    if not values:
        response = {
            'message': 'Nu am gasit date'
        }
        return jsonify(response), 400
    if 'block' not in values:
        response = {
            'message': 'Nu am toate datele'
        }
        return jsonify(response), 400
    block = values['block']
    print(block)
    if block['index'] == blockchain.chain[-1].index + 1:
        if blockchain.add_block(block):
            response = {
                'message': 'Block adaugat'
            }
            return jsonify(response), 201
        else:
            response = {
                'message': 'Block invalid'
            }
            return jsonify(response), 409
    elif block['index'] > blockchain.chain[-1].index:
        response = {
            'message': 'Blockchain-ul este diferit de cel local.'
        }
        blockchain.resolve_conflicts = True
        return jsonify(response), 200
    else:
        response = {
            'message': 'Blockchain-ul este scurt, adaugarea unui bloc a esuat'
        }
        return jsonify(response), 409


@app.route('/medie_semestriala', methods=['POST'])
def get_medie_semestriala():
    values = request.get_json()
    emitator = values['emitator']
    receptor = values['receptor']
    tip_unitate = values['tip_unitate']
    unitate_invatamant = values['unitate_invatamant']
    specializare = values['specializare']
    anul = values['anul']
    semestru = values['semestru']
    materie = values['materie']
    media = blockchain.get_medie_semestriala(
        emitator, receptor, tip_unitate, unitate_invatamant, specializare, anul, semestru, materie)
    if media != None:
        response = {
            'message': 'Calculul mediei a reusit',
            'rezultat': media
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'Calculul mediei a esuat. Nu am toate datele sau date valide'
        }
        return jsonify(response), 500


@app.route('/medie_anuala', methods=['POST'])
def get_medie_anuala():
    values = request.get_json()
    receptor = values['receptor']
    tip_unitate = values['tip_unitate']
    unitate_invatamant = values['unitate_invatamant']
    specializare = values['specializare']
    anul = values['anul']
    medie = blockchain.get_medie_anuala(
        receptor,
        tip_unitate,
        unitate_invatamant,
        specializare,
        anul)
    if medie != None:
        response = {
            'message': 'Calculul mediei a reusit',
            'rezultat': medie
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'Calculul mediei a esuat. Nu am toate datele sau date valide'
        }
        return jsonify(response), 500


@app.route('/rezultat_id', methods=['POST'])
def get_rezultate_pentru_id():
    values = request.get_json()
    if not values:
        response = {
            'message': 'Nu am gasit date'
        }
        return jsonify(response), 400
    rezultate = blockchain.get_rezultate(values['id'])
    if rezultate != None:
        response = {
            'message': 'Returnarea rezultate a reusit',
            'rezultate': [rez.to_ordered_dict() for rez in rezultate]
        }
        return jsonify(response), 200

    else:
        response = {
            'message': 'Returnarea rezultatelor a esuat',
            'carnet_set_up': carnet.public_key != None
        }
        return jsonify(response), 500


@app.route('/node', methods=['POST'])
def add_node():
    values = request.get_json()
    if not values:
        response = {
            'message': 'Nu am gasit date'
        }
        return jsonify(response), 400
    if 'node' not in values:
        response = {
            'message': 'Nu am nod atasat'
        }
        return jsonify(response), 400
    node = values['node']
    blockchain.add_peer_node(node)
    response = {
        'message': 'Nod atasat',
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 201


@app.route('/node/<node_url>', methods=['DELETE'])
def remove_node(node_url):
    if node_url == '' or node_url == None:
        response = {
            'message': 'Nu am gasit date'
        }
        return jsonify(response), 400
    blockchain.remove_peer_node(node_url)
    response = {
        'message': 'Nod sters',
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 200


@app.route('/nodes', methods=['GET'])
def get_nodes():
    response = {
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 200


@app.route('/profesor', methods=['POST'])
def add_profesor():
    values = request.get_json()
    if not values:
        response = {
            'message': 'Nu am gasit date'
        }
        return jsonify(response), 400
    if 'id' not in values:
        response = {
            'message': 'Nu am cheie atasata'
        }
        return jsonify(response), 400
    idProf = values['id']
    blockchain.add_profesor(idProf)
    response = {
        'message': 'Profesor atasat',
        'all_profesori': blockchain.get_profesori()
    }
    return jsonify(response), 201


@app.route('/profesor/<cheie>', methods=['DELETE'])
def remove_profesor(cheie):
    if cheie == '' or cheie == None:
        response = {
            'message': 'Nu am gasit date'
        }
        return jsonify(response), 400
    blockchain.remove_profesor(cheie)
    response = {
        'message': 'Nod sters',
        'all_profesori': blockchain.get_profesori()
    }
    return jsonify(response), 200


@app.route('/profesori', methods=['GET'])
def get_profesori():
    response = {
        'all_profesori': blockchain.get_profesori()
    }
    return jsonify(response), 200

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=51328)
    args = parser.parse_args()
    port = args.port
    carnet = Carnet(port)
    blockchain = Blockchain(carnet.public_key, port)
    app.run(host='0.0.0.0', port=port)
