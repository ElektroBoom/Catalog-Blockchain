from printable import Printable
from collections import OrderedDict


class Rezultat(Printable):
    def __init__(self, nume, materie, nota):
        self.nume = nume
        self.materie = materie
        self.nota = nota

    def __repr__(self):
        return str(self.__dict__)

    def to_ordered_dict(self):
        return OrderedDict([('nume', self.nume), ('materie', self.materie), ('nota', self.nota)])
