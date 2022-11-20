import math
import numpy as np
import textwrap
from typing import Callable

# a^e mod n
def fast_pow(a: int, e: int, n: int) -> int:
    res = 1
    for i in range(e):
        if((e >> i) % 2 == 1): 
            res = (res * a) % n
        a = (a*a) % n
        if 1 << i > e:
            break
    return res

def read_to_bin_str(path="../message.txt") -> str:
    ret = ""
    with open(path, 'r') as f:
        text = f.read()
        ret = ''.join(format(ord(x), '08b') for x in text)
    return ret

def encode_fn(bin_str: str, e: int, n:int) -> str:
    num = int(bin_str, 2)
    data_dec = fast_pow(num, e, n)
    return str(data_dec)

def encode(data: str, encode_fn: Callable[[str, int, int], str], chunck_size = 16) -> str:
    with open("./e_n.txt", "r") as keys:
        lines = [line[:-1] for line in keys.readlines()]
        e, n = [int(l) for l in lines]
    chunks = textwrap.wrap(data, chunck_size)
    encoded = map(encode_fn, chunks, [e]*len(chunks), [n]*len(chunks))
    dec_spaces = ' '.join(d for d in encoded) # decimal numbers with spaces
    ret = ''.join(format(ord(x), '08b') for x in dec_spaces)
    return ret

def write_file(bin_str: str, path="../message2.txt"):
    barray = []
    chuncks = textwrap.wrap(bin_str, 8)
    with open(path, "wb") as binary_file:
        for chunck in chuncks:
            barray.extend(bytes([int(chunck, 2)]))
        binary_file.write(bytes(barray))
    return

data_orig = read_to_bin_str()
print(data_orig)
encoded_bin_str = encode(data_orig, encode_fn)
write_file(encoded_bin_str)