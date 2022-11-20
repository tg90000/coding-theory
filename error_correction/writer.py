import numpy as np
import textwrap
from typing import Callable
import sys

def Hamming_7_4_G(bin_string: str) -> str:
    bin_string = bin_string.zfill(4)
    MTX = [
        [1,0,0,0,0,1,1],
        [0,1,0,0,1,0,1],
        [0,0,1,0,1,1,0],
        [0,0,0,1,1,1,1]]
    word = [int(s) for s in bin_string]
    G = np.array(MTX)
    w = np.array(word).transpose()
    code_word_vec = np.remainder(w @ G, 2)
    code_word = ''.join(str(i) for i in code_word_vec)
    return code_word

def encode(data: str, encode_fn: Callable[[str], str], chunck_size = 4) -> str:
    chunks = textwrap.wrap(data, chunck_size)
    encoded = map(encode_fn, chunks)
    return ''.join(d for d in encoded)

def write_file(bin_str: str, path="./data/data.txt"):
    barray = []
    chuncks = textwrap.wrap(bin_str, 8)
    with open(path, "wb") as binary_file:
        for chunck in chuncks:
            barray.extend(bytes([int(chunck, 2)]))
        binary_file.write(bytes(barray))
    return
    

def read_to_bin_str(path="./data/text.txt") -> str:
    ret = ""
    with open(path, 'r') as f:
        text = f.read()
        ret = ''.join(format(ord(x), '08b') for x in text)
    return ret


if __name__ == "__main__":
    # param spec
    input_str = read_to_bin_str()
    encoded_bin_str = encode(input_str, Hamming_7_4_G, 4)
    write_file(encoded_bin_str)