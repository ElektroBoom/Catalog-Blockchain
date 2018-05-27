from printable import Printable


class Rezultat(Printable):
    def __init__(self, nume, materie, nota):
        self.nume = nume
        self.materie = materie
        self.nota = nota

    def __repr__(self):
        return str(self.__dict__)
