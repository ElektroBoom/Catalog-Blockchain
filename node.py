from blockchain import Blockchain
from uuid import uuid4
from utility.verification import Verification
from utilizator import Utilizator
import pickle
from carnet import Carnet

nume_fisier = 'myself.ekb'


class Node:

    def __init__(self):
        self.carnet = Carnet()
        self.carnet.create_keys()
        self.blockchain = Blockchain(self.carnet.public_key)

    def load_user_data(self):
        incarcat = False
        try:
            with open(nume_fisier, mode='rb') as f:
                file_content = pickle.loads(f.read())
                self.carnet.public_key = file_content['me']
                incarcat = True
        except (IOError, IndexError):
            pass
        return incarcat

    def save_user_data(self):
        try:
            with open(nume_fisier, mode='wb') as f:
                saved_data = {'me': self.carnet.public_key}
                f.write(pickle.dumps(saved_data))
        except IOError:
            print('Saving fail!')

    def get_detalii_utilizator(self):
        nume = input('Numele dumneavoastra: ')
        prenume = input('Prenumele dumneavoastra:')
        cnp = input('CNP-ul dumneavoastra: ')
        self.blockchain.add_utilizatori(
            Utilizator(self.carnet.public_key, nume, prenume, cnp))

    def get_nota_value(self):
        receptor = input('Nume student: ')
        rezultat = float(input('Nota: '))
        return receptor, rezultat

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
            print('4: Citeste si inregistreaza-ma')
            print('5: afiseaza persoane')
            print('6: Creaza carnet')
            print('7: Incarca carnet')
            print('8: Salveaza chei')
            print('q: Opreste executia programului')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_rezultate = self.get_nota_value()
                receptor, info_didactic = tx_rezultate
                signature = self.carnet.sign(
                    self.carnet.public_key, receptor, info_didactic)
                self.blockchain.add_nota(
                    self.carnet.public_key, receptor, info_didactic, signature)
                print(self.blockchain.get_date_de_introdus)
            elif user_choice == '2':
                if not self.blockchain.mine_block():
                    print('Minarea a esuat!')
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                self.get_detalii_utilizator()
            elif user_choice == '5':
                print(self.blockchain.utilizatori)
            elif user_choice == '6':
                self.carnet.create_keys()
                self.blockchain = Blockchain(self.carnet.public_key)
            elif user_choice == '7':
                self.carnet.load_keys()
                self.blockchain = Blockchain(self.carnet.public_key)
            elif user_choice == '8':
                self.carnet.save_keys()
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

    # if not node.load_user_data():
    #     node.save_user_data()

    #     trebuie_inregistrat = False
    #     if len(node.blockchain.utilizatori) > 0:
    #         for utilizator in node.blockchain.utilizatori:
    #             print('{} {}'.format(utilizator.id, node.carnet.public_key))

    #             if not utilizator.id == node.carnet.public_key:

    #                 trebuie_inregistrat = True
    #                 break
    #     else:
    #         trebuie_inregistrat = True
    #     if trebuie_inregistrat:
    #         node.get_detalii_utilizator()

    node.listen_for_input()
