import json
from os import path as p

def decode_json(path):
    with open(path) as f:
        j = json.load(f)
    return j

def encode_json(j, path):
    with open(path, "w") as f:
        json.dump(j, f, indent= 4)
    return j
