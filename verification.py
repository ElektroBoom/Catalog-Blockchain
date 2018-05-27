from hash_util import hash_block, hash_string_256

dificultate = 2


class Verification:
    def verify_chain(self, blockchain):
        for (index, block) in enumerate(blockchain):
            print('block rezultate', block.rezultate)
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index-1]):
                return False
            if not self.valid_proof(block.rezultate, block.previous_hash, block.proof):
                print('PoW invalid!')
                return False
        return True

    def valid_proof(self, rezultate, last_hash, proof):
        guess = (str(rezultate) + str(last_hash) + str(proof)).encode()
        guess_hash = hash_string_256(guess)
        isValid = guess_hash[:2] == '0' * dificultate
        return isValid
