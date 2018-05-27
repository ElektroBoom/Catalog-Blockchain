import hashlib as hl
import json


def hash_string_256(string):
    return hl.sha256(string).hexdigest()


def hash_block(block):
    hashable_block = block.__dict__.copy()
    return hl.sha256(json.dumps(hashable_block, sort_keys=True).encode()).hexdigest()
