import hashlib as hl
import json
from collections import OrderedDict
import pickle

from hash_util import hash_block, hash_string_256

genesis_block = {'previous_hash': '',
                 'index': 0,
                 'rezultate': [],
                 'proof': 123
                 }
blockchain = [genesis_block]
date_de_introdus = []
dificultate = 2
nume_fisier = 'blockchain.txt'


def load_data():
    with open(nume_fisier, mode='r') as f:
        # file_content = pickle.loads(f.read())
        file_content = f.readlines()

        global blockchain
        global date_de_introdus

        # blockchain = file_content['chain']
        # date_de_introdus = file_content['rez']
        blockchain = json.loads(file_content[0][:-1])
        blockchain = [{'previous_hash': block['previous_hash'],
                       'index': block['index'],
                       'proof': block['proof'],
                       'rezultate': [OrderedDict([('nume', rez['nume']),
                                                  ('materie', rez['materie']),
                                                  ('nota', rez['nota'])])
                                     for rez in block['rezultate']]} for block in blockchain]
        date_de_introdus = json.loads(file_content[1])
        date_de_introdus = [OrderedDict([('nume', rez['nume']),
                                         ('materie', rez['materie']),
                                         ('nota', rez['nota'])])
                            for rez in date_de_introdus]


# load_data()


def save_data():
    with open(nume_fisier, mode='w') as f:
        f.write(json.dumps(blockchain))
        f.write('\n')
        f.write(json.dumps(date_de_introdus))
        # saved_data = {'chain': blockchain,
        #               'rez': date_de_introdus}
        # f.write(pickle.dumps(saved_data))


def valid_proof(date_de_introdus, last_hash, proof):
    print()
    guess = (str(date_de_introdus) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    isValid = guess_hash[:2] == '0' * dificultate
    print('Proof of work pentru {}\n{}\n{}\neste {}'.format(
        date_de_introdus, last_hash, proof, isValid))
    return isValid


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(date_de_introdus, last_hash, proof):
        proof += 1
    return proof


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_nota(nume, materie, nota):
    mark = OrderedDict([('nume', nume), ('materie', materie), ('nota', nota)])
    date_de_introdus.append(mark)
    save_data()


def mine_block():
    hashed_last_block = hash_block(get_last_blockchain_value())
    print('hashed last block', hashed_last_block)
    proof = proof_of_work()
    print('proof of work', proof)
    block = {'previous_hash': hashed_last_block,
             'index': len(blockchain),
             'rezultate': date_de_introdus,
             'proof': proof
             }
    blockchain.append(block)
    return True


def get_nota_value():
    nume = input('Nume student: ')
    materie = input('Denumire materie: ')
    nota = float(input('Nota: '))
    return nume, materie, nota


def get_user_choice():
    return input('Alegerea dumneavoastra: ')


def print_blockchain_elements():
    for block in blockchain:
        print('Printez block')
        print(block)
    else:
        print('-' * len(str(block)))


def verify_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index-1]):
            return False
        if not valid_proof(block['rezultate'], block['previous_hash'], block['proof']):
            print('PoW invalid!')
            return False
    return True


waiting_for_input = True

while waiting_for_input:
    print('Alegeti o optiune:')
    print('1: Adauga o nota')
    print('2: Mineaza blocuri')
    print('3: Afiseaza blocuri blockchain')
    print('4: Elevi inregistrati')
    print('h: Manipuleaza date blockchain')
    print('q: Opreste executia programului')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_rezultate = get_nota_value()
        nume, materie, nota = tx_rezultate
        add_nota(nume, materie, nota)
        print(date_de_introdus)
    elif user_choice == '2':
        if mine_block():
            date_de_introdus = []
            save_data()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {'previous_hash': '',
                             'index': 0,
                             'rezultate': [{'nume': 'Iulian', 'materie': 'Info', 'nota': '10'}]}
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Optiune inexistenta!')
    if not verify_chain():
        print_blockchain_elements()
        print('Blockchain-ul este invalid!')
        break
else:
    print('Utilizatorul a iesit!')

print("Gata!")
