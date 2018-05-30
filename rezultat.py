from utility.printable import Printable
from collections import OrderedDict


class Rezultat(Printable):
    def __init__(self, emitator, receptor, rezultat):
        self.emitator = emitator
        self.receptor = receptor
        self.rezultat = rezultat

    def __repr__(self):
        return str(self.__dict__)

    def to_ordered_dict(self):
        return OrderedDict([('emitator', self.emitator), ('receptor', self.receptor), ('rezultat', self.rezultat)])
