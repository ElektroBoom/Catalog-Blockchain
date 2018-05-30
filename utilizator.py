from utility.printable import Printable
from collections import OrderedDict


class Utilizator(Printable):
    def __init__(self, id, nume, prenume, cnp):
        self.id = id
        self.nume = nume
        self.prenume = prenume
        self.cnp = cnp
