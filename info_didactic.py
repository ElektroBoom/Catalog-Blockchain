from utility.printable import Printable


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
