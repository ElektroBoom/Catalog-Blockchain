import hashlib as hl
import json
from collections import OrderedDict
import pickle

from hash_util import hash_block, hash_string_256
from block import Block


blockchain = []
date_de_introdus = []

dificultate = 2
nume_fisier = 'blockchain.ekb'


def load_data():
    global blockchain
    global date_de_introdus
    try:
        with open(nume_fisier, mode='rb') as f:
            file_content = pickle.loads(f.read())
            # file_content = f.readlines()
            blockchain = file_content['chain']
            date_de_introdus = file_content['rez']
            # blockchain = json.loads(file_content[0][:-1])
            # blockchain = [{'previous_hash': block['previous_hash'],
            #                'index': block['index'],
            #                'proof': block['proof'],
            #                'rezultate': [OrderedDict([('nume', rez['nume']),
            #                                           ('materie',
            #                                            rez['materie']),
            #                                           ('nota', rez['nota'])])
            #                              for rez in block['rezultate']]} for block in blockchain]
            # date_de_introdus = json.loads(file_content[1])
            # date_de_introdus = [OrderedDict([('nume', rez['nume']),
            #                                  ('materie', rez['materie']),
            #                                  ('nota', rez['nota'])])
            #                     for rez in date_de_introdus]
    except (IOError, IndexError):
        genesis_block = Block(0, '', [], 123, 0)
        blockchain = [genesis_block]
        date_de_introdus = []


load_data()


def save_data():
    try:
        with open(nume_fisier, mode='wb') as f:
            # f.write(json.dumps(blockchain))
            # f.write('\n')
            # f.write(json.dumps(date_de_introdus))
            saved_data = {'chain': blockchain,
                          'rez': date_de_introdus}
            f.write(pickle.dumps(saved_data))
    except IOError:
        print('Saving fail!')


def valid_proof(rezultate, last_hash, proof):
    guess = (str(rezultate) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    isValid = guess_hash[:2] == '0' * dificultate
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
    proof = proof_of_work()
    block = Block(len(blockchain), hashed_last_block, date_de_introdus, proof)
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
        print('-' * 90)


def verify_chain():
    for (index, block) in enumerate(blockchain):
        print('block rezultate', block.rezultate)
        if index == 0:
            continue
        if block.previous_hash != hash_block(blockchain[index-1]):
            return False
        if not valid_proof(block.rezultate, block.previous_hash, block.proof):
            print('PoW invalid!')
            return False
    return True


waiting_for_input = True

while waiting_for_input:
    print('Alegeti o optiune:')
    print('1: Adauga o nota')
    print('2: Mineaza blocuri')
    print('3: Afiseaza blocuri blockchain')
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
