from utility.printable import Printable
from collections import OrderedDict


class InfoDidactic(Printable):
    def __init__(self, tip_info, materie, descriere,  nota, an_scolar, data_intamplarii, unitate_invatamant, specializare, comentariu):
        self.tip_info = tip_info
        self.materie = materie
        self.descriere = descriere
        self.nota = nota
        self.an_scolar = an_scolar
        self.data_intamplarii = data_intamplarii
        self.unitate_invatamant = unitate_invatamant
        self.specializare = specializare
        self.comentariu = comentariu

    def to_ordered_dict(self):
        return OrderedDict([('tip_info', self.tip_info),
                            ('materie', self.materie),
                            ('rezultat', self.descriere),
                            ('rezultat', self.nota),
                            ('rezultat', self.an_scolar),
                            ('rezultat', self.data_intamplarii),
                            ('rezultat', self.unitate_invatamant),
                            ('rezultat', self.specializare),
                            ('rezultat', self.comentariu)])
