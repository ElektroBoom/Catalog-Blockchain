from utility.printable import Printable
from collections import OrderedDict


class InfoDidactic(Printable):
    """Clasa ce memoreaza """

    def __init__(self, tip_info, materie, descriere,  nota, credite, an_scolar, semestru, data_intamplarii, tip_unitate, unitate_invatamant, specializare, comentariu):
        self.tip_info = tip_info
        self.materie = materie
        self.descriere = descriere
        self.nota = nota
        self.credite = credite
        self.an_scolar = an_scolar
        self.semestru = semestru
        self.data_intamplarii = data_intamplarii
        self.tip_unitate = tip_unitate
        self.unitate_invatamant = unitate_invatamant
        self.specializare = specializare
        self.comentariu = comentariu

    def to_ordered_dict(self):
        return OrderedDict([('tip_info', self.tip_info),
                            ('materie', self.materie),
                            ('descriere', self.descriere),
                            ('nota', self.nota),
                            ('credite', self.credite),
                            ('an_scolar', self.an_scolar),
                            ('semestru', self.semestru),
                            ('data_intamplarii', self.data_intamplarii),
                            ('tip_unitate', self.tip_unitate),
                            ('unitate_invatamant', self.unitate_invatamant),
                            ('specializare', self.specializare),
                            ('comentariu', self.comentariu)])
