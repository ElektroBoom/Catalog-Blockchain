import hashlib as hl
import json
import pickle

from utility.verification import Verification
from utility.hash_util import hash_block
from block import Block
from rezultat import Rezultat
from carnet import Carnet

nume_fisier = 'blockchain.ekb'


class Blockchain:
    def __init__(self, hosting_node_id):
        genesis_block = Block(0, '', [], 123, 0)
        self.chain = [genesis_block]
        self.__date_de_introdus = []
        self.utilizatori = []
        self.load_data()
        self.hosting_node = hosting_node_id

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_utili4zatori(self):
        return self.utilizatori[:]

    def add_utilizatori(self, val):
        if len(self.utilizatori) > 0:
            for utilizator in self.utilizatori:
                print(utilizator)
                if not val.cnp == utilizator.cnp:
                    self.utilizatori.append(val)
                else:
                    print('CNP-ul exista deja!')
        else:
            self.utilizatori.append(val)

    def get_date_de_introdus(self):
        self.__date_de_introdus[:]

    def load_data(self):
        try:
            with open(nume_fisier, mode='rb') as f:
                file_content = pickle.loads(f.read())
                # file_content = f.readlines()
                self.chain = file_content['chain']
                self.__date_de_introdus = file_content['rez']
                self.utilizatori = file_content['utilizatori']
        except (IOError, IndexError):
            pass

    def get_rezultate(self, receptor='123'):
        lista_note = []
        for block in self.chain:
            print(block)
            for rez in block.rezultate:
                print(rez)
                if rez.receptor == receptor:
                    lista_note.append(rez.info_didactic)
        print('lista de note este', lista_note)

    def save_data(self):
        try:
            with open(nume_fisier, mode='wb') as f:
                saved_data = {'chain': self.chain,
                              'rez': self.__date_de_introdus,
                              'utilizatori': self.utilizatori}
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

    def add_nota(self, emitator, receptor, info_didactic, signature):
        if self.hosting_node == None:
            return False
        rezultat = Rezultat(emitator, receptor, info_didactic, signature)
        if not Carnet.verify_rezultat(rezultat):
            return False
        self.__date_de_introdus.append(rezultat)
        self.save_data()

    def mine_block(self):
        if self.hosting_node == None:
            return None
        hashed_last_block = hash_block(self.get_last_blockchain_value())
        proof = self.proof_of_work()
        block = Block(len(self.__chain), hashed_last_block,
                      self.__date_de_introdus, proof)
        for rez in block.rezultate:
            if not Carnet.verify_rezultat(rez):
                return None
        self.__chain.append(block)
        self.__date_de_introdus = []
        self.save_data()
        return block
