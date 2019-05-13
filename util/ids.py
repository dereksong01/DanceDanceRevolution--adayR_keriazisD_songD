from random import choice
from string import ascii_letters, digits

Id = str

charpool = ascii_letters + digits + '-_'

def gen_id(length: int) -> Id:
    return ''.join([choice(charpool) for _ in range(length)])

