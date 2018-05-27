from blockchain import Blockchain
from uuid import uuid4
from verification import Verification


class Node:

    def __init__(self):
        self.id = str(uuid4())
        self.blockchain = Blockchain(self.id)

    def get_nota_value(self):
        nume = input('Nume student: ')
        materie = input('Denumire materie: ')
        nota = float(input('Nota: '))
        return nume, materie, nota

    def get_user_choice(self):
        return input('Alegerea dumneavoastra: ')

    def print_blockchain_elements(self):
        for block in self.blockchain.get_chain():
            print('Printez block')
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
            print('q: Opreste executia programului')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_rezultate = self.get_nota_value()
                nume, materie, nota = tx_rezultate
                self.blockchain.add_nota(nume, materie, nota)
                print(self.blockchain.get_date_de_introdus)
            elif user_choice == '2':
                self.blockchain.mine_block()
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == 'q':
                waiting_for_input = False
            else:
                print('Optiune inexistenta!')
            if not Verification.verify_chain(self.blockchain.get_chain()):
                self.print_blockchain_elements()
                print('Blockchain-ul este invalid!')
                break
        else:
            print('Utilizatorul a iesit!')


node = Node()
node.listen_for_input()
