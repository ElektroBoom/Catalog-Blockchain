from utility.printable import Printable
from collections import OrderedDict
from info_didactic import InfoDidactic


class Rezultat(Printable):
    def __init__(self, emitator, receptor, info_didactic, semnatura):
        self.emitator = emitator
        self.receptor = receptor
        self.info_didactic = info_didactic
        self.semnatura = semnatura

    def to_ordered_dict(self):
        return OrderedDict([('emitator', self.emitator), ('receptor', self.receptor), ('info_didactic',  self.info_didactic.to_ordered_dict() if type(self.info_didactic) is InfoDidactic else self.info_didactic), ('semnatura', self.semnatura)])
