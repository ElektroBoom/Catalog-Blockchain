from carnet import Carnet
from blockchain import Blockchain
from uuid import uuid4
from utility.verification import Verification
from utilizator import Utilizator
import pickle
from carnet import Carnet
from info_didactic import InfoDidactic

nume_fisier = 'carnet.txt'


class Node:

    def __init__(self):
        self.carnet = Carnet()
        self.blockchain = Blockchain(self.carnet.public_key)

    def load_user_data(self):
        incarcat = False
        try:
            with open(nume_fisier, mode='r') as f:
                file_content = f.readlines()
                self.carnet.public_key = file_content[0][:-1]
                incarcat = True
        except (IOError, IndexError):
            pass
        return incarcat

    def get_detalii_utilizator(self):
        nume = input('Numele dumneavoastra: ')
        prenume = input('Prenumele dumneavoastra:')
        cnp = input('CNP-ul dumneavoastra: ')
        self.blockchain.add_utilizatori(
            Utilizator(self.carnet.public_key, nume, prenume, cnp))

    def get_nota_value(self):
        receptor = input('id student: ')
        tip_info = input('tip_info ')
        materie = input('materie ')
        descriere = input('descriere ')
        nota = input('nota ')
        an_scolar = input('an_scolar ')
        semestru = input('semestru ')
        data_intamplarii = input('data_intamplarii ')
        tip_unitate = input('tip_unitate')
        unitate_invatamant = input('unitate_invatamant ')
        specializare = input('specializare ')
        comentariu = input('comentariu ')
        return receptor, InfoDidactic(tip_info, materie, descriere,  nota, an_scolar, semestru, data_intamplarii, tip_unitate, unitate_invatamant, specializare, comentariu)

    def get_user_choice(self):
        return input('Alegerea dumneavoastra: ')

    def print_blockchain_elements(self):
        for block in self.blockchain.chain:
            print(block)
        else:
            print('-' * 90)

    def listen_for_input(self):
        waiting_for_input = True

        while waiting_for_input:
            print('Alegeti o optiune:')
            print('1: Adauga o nota')
            print('2: Mineaza blocuri')
            print('3: Afiseaza blocuri blockchain')
            print('4: afiseaza persoane')
            print('5: Creaza carnet')
            print('6: Incarca carnet')
            print('7: Salveaza chei')
            print('8: Lista rezultate')
            print('9: Afiseaaza date de introdus')
            print('10: Medie')
            print('q: Opreste executia programului')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_rezultate = self.get_nota_value()
                receptor, nota = tx_rezultate
                semnatura = self.carnet.sign_rezultat(
                    self.carnet.public_key, receptor, nota)
                self.blockchain.add_nota(
                    self.carnet.public_key, receptor, nota, semnatura)
                print(self.blockchain.get_date_de_introdus)
            elif user_choice == '2':
                if not self.blockchain.mine_block():
                    print('Minarea a esuat')
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                print(self.blockchain.utilizatori)
            elif user_choice == '5':
                self.carnet.create_keys()
                self.blockchain = Blockchain(self.carnet.public_key)
            elif user_choice == '6':
                self.carnet.load_keys()
                self.blockchain = Blockchain(self.carnet.public_key)
            elif user_choice == '7':
                self.carnet.save_keys()
            elif user_choice == '8':
                self.blockchain.get_rezultate('123')
            elif user_choice == '9':
                dateele = self.blockchain.get_date_de_introdus()
                print(dateele)
            elif user_choice == '10':
                print(self.blockchain.get_medie_semestriala(
                    '123', 'aciee', 'cti', '2', '2', 'pclp'))
            elif user_choice == 'q':
                waiting_for_input = False
            else:
                print('Optiune inexistenta!')
            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print('Blockchain-ul este invalid!')
                break
        else:
            print('Utilizatorul a iesit!')


if __name__ == '__main__':
    node = Node()

    if not node.load_user_data():

        trebuie_inregistrat = False
        if len(node.blockchain.utilizatori) > 0:
            for utilizator in node.blockchain.utilizatori:
                print('{} {}'.format(utilizator.id, node.carnet.public_key))

                if not utilizator.id == node.carnet.public_key:

                    trebuie_inregistrat = True
                    break
        else:
            trebuie_inregistrat = True
        if trebuie_inregistrat:
            node.get_detalii_utilizator()

    node.listen_for_input()
