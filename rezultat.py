from utility.printable import Printable
from collections import OrderedDict


class Rezultat(Printable):
    def __init__(self, emitator, receptor, info_didactic, signature):
        self.emitator = emitator
        self.receptor = receptor
        self.info_didactic = info_didactic
        self.signature = signature

    def __repr__(self):
        return str(self.__dict__)

    def to_ordered_dict(self):
        return OrderedDict([('emitator', self.emitator), ('receptor', self.receptor), ('rezultat', self.info_didactic.to_ordered_dict())])
