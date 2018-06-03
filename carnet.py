from Crypto.PublicKey import RSA
import Crypto.Random
import binascii


class Carnet:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key
    
    def load_keys(self):
<<<<<<< HEAD
        try:
            with open('carnet.txt', mode='r') as f:
                keys = f.readlines()
                public_key = keys[0][:-1]
                private_key = keys[1]
                self.public_key = public_key
                self.private_key = private_key
        except(IOError, IndexError):
            print('Incarcarea cheilor a esuat!')
=======
        pass
>>>>>>> parent of 14b7674... carnet & signature use

    def generate_keys(self):
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        return (binascii.hexlify(private_key.exportKey(format='DER').decode('ascii')),
                binascii.hexlify(public_key.exportKey(format='DER').decode('ascii')))
