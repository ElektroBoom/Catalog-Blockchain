from time import time


class Block:

    def __init__(self, index, previous_hash, rezultate, proof, time=time()):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time
        self.rezultate = rezultate
        self.proof = proof

    def __str__(self):
        return 'Block nr. {}\nprevious_hash {}\ntimestamp {}\nrezultate {}\nproof {}'.format(
            self.index, self.previous_hash, self.timestamp, self.rezultate, self.proof)
