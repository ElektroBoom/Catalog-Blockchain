import hashlib as hl
import json
import pickle

from utility.verification import Verification
from utility.hash_util import hash_block
from block import Block
from rezultat import Rezultat

nume_fisier = 'blockchain.ekb'


class Blockchain:
    def __init__(self, hosting_node_id):
        genesis_block = Block(0, '', [], 123, 0)
        self.chain = [genesis_block]
        self.__date_de_introdus = []
        self.load_data()
        self.hosting_node = hosting_node_id

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_date_de_introdus(self):
        self.__date_de_introdus[:]

    def load_data(self):
        try:
            with open(nume_fisier, mode='rb') as f:
                file_content = pickle.loads(f.read())
                # file_content = f.readlines()
                self.chain = file_content['chain']
                self.__date_de_introdus = file_content['rez']
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
            pass

    def save_data(self):
        try:
            with open(nume_fisier, mode='wb') as f:
                # f.write(json.dumps(blockchain))
                # f.write('\n')
                # f.write(json.dumps(date_de_introdus))
                saved_data = {'chain': self.__chain,
                              'rez': self.__date_de_introdus}
                f.write(pickle.dumps(saved_data))
        except IOError:
            print('Saving fail!')

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__date_de_introdus, last_hash, proof):
            proof += 1
        return proof

    def get_last_blockchain_value(self):
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_nota(self, nume, materie, nota):
        mark = Rezultat(nume, materie, nota)
        self.__date_de_introdus.append(mark)
        self.save_data()

    def mine_block(self):
        hashed_last_block = hash_block(self.get_last_blockchain_value())
        proof = self.proof_of_work()
        block = Block(len(self.__chain), hashed_last_block,
                      self.__date_de_introdus, proof)
        self.__chain.append(block)
        self.__date_de_introdus = []
        self.save_data()
        return True


print("Gata!")
