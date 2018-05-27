from time import time

from utility.printable import Printable


class Block(Printable):

    def __init__(self, index, previous_hash, rezultate, proof, time=time()):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time
        self.rezultate = rezultate
        self.proof = proof
