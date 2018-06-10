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
                    return True
                else:
                    print('CNP-ul exista deja!')
                    return False
        else:
            self.utilizatori.append(val)
            return True

    def get_date_de_introdus(self):
        return self.__date_de_introdus[:]

    def load_data(self):
        try:
            with open(nume_fisier, mode='rb') as f:
                file_content = pickle.loads(f.read())
                self.chain = file_content['chain']
                self.__date_de_introdus = file_content['rez']
                self.utilizatori = file_content['utilizatori']
        except (IOError, IndexError):
            pass

    def save_data(self):
        try:
            with open(nume_fisier, mode='wb') as f:
                saved_data = {'chain': self.chain,
                              'rez': self.__date_de_introdus,
                              'utilizatori': self.utilizatori}
                f.write(pickle.dumps(saved_data))
        except IOError:
            print('Saving fail!')

    def get_rezultate(self, id):
        if self.hosting_node == None:
            return None
        lista_rezultate = []
        for block in self.chain:
            for rez in block.rezultate:
                if rez.receptor == id:
                    lista_rezultate.append(rez)
        return lista_rezultate

    def get_medie_semestriala(self, emitator, receptor, tip_unitate, unitate_invatamant, specializare, anul, semestru, materie):
        lista_rezultate = []
        lista_credite = []
        for block in self.chain:
            for rez in block.rezultate:
                if rez.receptor == receptor and rez.emitator == emitator and rez.info_didactic.tip_unitate == tip_unitate and rez.info_didactic.unitate_invatamant == unitate_invatamant and rez.info_didactic.specializare == specializare and rez.info_didactic.an_scolar == anul and rez.info_didactic.semestru == semestru and rez.info_didactic.materie == materie and rez.info_didactic.tip_info == 'Nota':
                    lista_rezultate.append(
                        float(rez.info_didactic.nota) * float(rez.info_didactic.credite))
                    lista_credite.append(float(rez.info_didactic.credite))
        lista_rezultate = [float(elem) for elem in lista_rezultate]
        print(lista_rezultate)
        if len(lista_credite) > 0:
            return sum(lista_rezultate)/sum(lista_credite)
        else:
            return None

    def get_medie_anuala(self, emitator, receptor, tip_unitate, unitate_invatamant, specializare, anul):
        pass

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

    def add_nota(self, emitator, receptor, info_didactic, semnatura):
        if self.hosting_node == None:
            return False
        rezultat = Rezultat(emitator, receptor, info_didactic, semnatura)
        if not Carnet.verify_rezultat(rezultat):
            return False
        self.__date_de_introdus.append(rezultat)
        self.save_data()
        return True

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
