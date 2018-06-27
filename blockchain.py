import json
import pickle
import requests
from utility.verification import Verification
from utility.hash_util import hash_block
from block import Block
from rezultat import Rezultat
from carnet import Carnet
from info_didactic import InfoDidactic


class Blockchain:
    def __init__(self, public_key, node_id):
        genesis_block = Block(0, '', [], 123, 0)
        self.chain = [genesis_block]
        self.__date_de_introdus = []
        self.profesori = set()
        self.public_key = public_key
        self.__peer_nodes = set()
        self.node_id = node_id
        self.resolve_conflicts = False
        self.load_data()

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def add_prof_incredere(self, val):
        self.profesori.add(val)
        return True

    def get_date_de_introdus(self):
        return self.__date_de_introdus[:]

    def load_data(self):
        try:
            with open('blockchain-{}.ekb'.format(self.node_id), mode='rb') as f:
                file_content = pickle.loads(f.read())
                self.chain = file_content['chain']
                self.__date_de_introdus = file_content['rez']
                self.profesori = file_content['profesori']
                self.__peer_nodes = file_content['noduri']
        except (IOError, IndexError):
            pass

    def save_data(self):
        try:
            with open('blockchain-{}.ekb'.format(self.node_id), mode='wb') as f:
                for block in self.chain:
                    for rez in block.rezultate:
                        if not type(rez.info_didactic) is InfoDidactic:
                            info_didactic_data = rez.info_didactic
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
                            rez.info_didactic = info_didactic
                saved_data = {'chain': self.chain,
                              'rez': self.__date_de_introdus,
                              'profesori': self.profesori,
                              'noduri': self.__peer_nodes
                              }
                f.write(pickle.dumps(saved_data))
        except IOError:
            print('Saving fail!')

    def get_rezultate(self, id):
        if self.public_key == None:
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
                    lista_rezultate.append(float(rez.info_didactic.nota) * (float(
                        rez.info_didactic.credite) if rez.info_didactic.tip_unitate == 'univeristate' else 1))

                    lista_credite.append(float(
                        rez.info_didactic.credite) if rez.info_didactic.tip_unitate == 'univeristate' else 1)
        lista_rezultate = [float(elem) for elem in lista_rezultate]
        if len(lista_credite) > 0:
            return sum(lista_rezultate)/sum(lista_credite)
        else:
            return None

    def get_medie_anuala(self, receptor, tip_unitate, unitate_invatamant, specializare, anul):
        lista_rezultate = []
        lista_credite = []
        for block in self.chain:
            for rez in block.rezultate:
                if not type(rez.info_didactic) is InfoDidactic:
                    info_didactic_data = rez.info_didactic
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
                    rez.info_didactic = info_didactic
                if rez.receptor == receptor and rez.emitator in self.profesori and rez.info_didactic.tip_unitate == tip_unitate and rez.info_didactic.unitate_invatamant == unitate_invatamant and rez.info_didactic.specializare == specializare and rez.info_didactic.an_scolar == anul and rez.info_didactic.tip_info == 'Nota':
                    lista_rezultate.append(float(rez.info_didactic.nota) * (float(
                        rez.info_didactic.credite) if rez.info_didactic.tip_unitate == 'universitate' else 1))

                    lista_credite.append(float(
                        rez.info_didactic.credite) if rez.info_didactic.tip_unitate == 'universitate' else 1)
        lista_rezultate = [float(elem) for elem in lista_rezultate]
        if len(lista_credite) > 0:
            return sum(lista_rezultate)/sum(lista_credite)
        else:
            return None

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

    def add_nota(self, emitator, receptor, info_didactic, semnatura, is_receiving=False):
        rezultat = Rezultat(emitator, receptor, info_didactic, semnatura)
        print(rezultat)
        if not Carnet.verify_rezultat(rezultat):
            return False
        self.__date_de_introdus.append(rezultat)
        self.save_data()
        if not is_receiving:
            for node in self.__peer_nodes:
                url = 'http://{}/broadcast_note'.format(node)
                try:
                    response = requests.post(url, json={'emitator': emitator,
                                                        'receptor': receptor,
                                                        'info_didactic': info_didactic.to_ordered_dict(),
                                                        'semnatura': semnatura
                                                        })
                    if response.status_code == 400 or response.status_code == 500:
                        print('nota aiurea')
                        return False
                except requests.exceptions.ConnectionError:
                    continue
        return True

    def mine_block(self):
        if self.public_key == None:
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
        for node in self.__peer_nodes:
            url = 'http://{}/broadcast_block'.format(node)
            block_convertit = block.__dict__.copy()
            block_convertit['rezultate'] = [rez.to_ordered_dict()
                                            for rez in block_convertit['rezultate']]
            try:
                response = requests.post(url, json={'block': block_convertit})
                if response.status_code == 400 or response.status_code == 500:
                    print('bloc aiurea')
                if response.status_code == 409:
                    self.resolve_conflicts = True
            except requests.exceptions.ConnectionError:
                continue
        return block

    def add_block(self, block):
        rezultate = [Rezultat(rez['emitator'], rez['receptor'], rez['info_didactic'],
                              rez['semnatura']) for rez in block['rezultate']]
        proof_valid = Verification.valid_proof(
            rezultate, block['previous_hash'], block['proof'])
        hashes_match = hash_block(self.chain[-1]) == block['previous_hash']
        if not proof_valid or not hashes_match:
            return False
        bloc_convertit = Block(
            block['index'], block['previous_hash'], rezultate,  block['proof'], block['timestamp'])
        self.__chain.append(bloc_convertit)
        stored_rezultate = self.__date_de_introdus[:]
        for dDI in block['rezultate']:
            for openDate in stored_rezultate:
                if openDate.emitator == dDI['emitator'] and openDate.receptor == dDI['receptor'] and openDate.semnatura == dDI['semnatura']:
                    try:
                        self.__date_de_introdus.remove(openDate)
                    except ValueError:
                        print('Element deja eliminat')
        self.save_data()
        return True

    def resolve(self):
        winner_chain = self.chain
        replace = False
        for node in self.__peer_nodes:
            url = 'http://{}/chain'.format(node)
            try:
                response = requests.get(url)
                node_chain = response.json()
                node_chain = [Block(block['index'],
                                    block['previous_hash'],
                                    [Rezultat(rez['emitator'],
                                              rez['receptor'],
                                              InfoDidactic(rez['info_didactic']['tip_info'],
                                                           rez['info_didactic']['materie'],
                                                           rez['info_didactic']['descriere'],
                                                           rez['info_didactic']['nota'],
                                                           rez['info_didactic']['credite'],
                                                           rez['info_didactic']['an_scolar'],
                                                           rez['info_didactic']['semestru'],
                                                           rez['info_didactic']['data_intamplarii'],
                                                           rez['info_didactic']['tip_unitate'],
                                                           rez['info_didactic']['unitate_invatamant'],
                                                           rez['info_didactic']['specializare'],
                                                           rez['info_didactic']['comentariu']),
                                              rez['semnatura']) for rez in block['rezultate']],
                                    block['proof'],
                                    block['timestamp']) for block in node_chain]
                node_chain_length = len(node_chain)
                local_chain_length = len(winner_chain)
                if node_chain_length > local_chain_length and Verification.verify_chain(node_chain):
                    winner_chain = node_chain
                    replace = True
            except requests.exceptions.ConnectionError:
                continue
        self.resolve_conflicts = False
        self.chain = winner_chain
        if replace:
            self.__date_de_introdus = []
        self.save_data()
        return replace

    def add_peer_node(self, node):
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_peer_nodes(self):
        return list(self.__peer_nodes)

    def add_profesor(self, cheie):
        self.profesori.add(cheie)
        self.save_data()

    def remove_profesor(self, cheie):
        self.profesori.discard(cheie)
        self.save_data()

    def get_profesori(self):
        return list(self.profesori)
