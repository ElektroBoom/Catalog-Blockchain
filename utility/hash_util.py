import hashlib as hl
import json


def hash_string_256(string):
    return hl.sha256(string).hexdigest()


def hash_block(block):
    hashable_block = block.__dict__.copy()
    hashable_block['rezultate'] = [rez.to_ordered_dict()
                                   for rez in hashable_block['rezultate']]

    return hl.sha256(json.dumps(hashable_block, sort_keys=True).encode()).hexdigest()
