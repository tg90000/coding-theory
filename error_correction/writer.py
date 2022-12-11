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

def read_one(path="./data/text_one.txt")-> list[int]:
    with open(path, "r") as f:
        data = f.readline()
        vec = [int(c) for c in data]
        return vec

def encode_one(G: list[list[int]], word: list[int], zn: int) -> list[int]:
    w = np.array(word).transpose()
    return (np.remainder(w @ np.array(G), zn)).tolist()

def write_one(w: list[int], path="./data/data_one.txt") -> None:
    with open(path, "w") as f:
        string = "".join(str(c) for c in w)
        f.write(string)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        input_str = read_to_bin_str()
        encoded_bin_str = encode(input_str, Hamming_7_4_G, 4)
        write_file(encoded_bin_str)
    elif sys.argv[1] == "test1":
        # word example: 12
        test_generator = [[1,0,2,2], [0,1,2,1]]
        zn = 3
        word = read_one()
        encoded = encode_one(test_generator, word, zn)
        write_one(encoded)
    elif sys.argv[1] == "test2":
        # word example: 110011001010
        test_generator = [
            [1,0,0,0,0,0,0,0,0,0,0,0, 0,1,1,1,1,1,1,1,1,1,1,1],
            [0,1,0,0,0,0,0,0,0,0,0,0, 1,1,1,0,1,1,1,0,0,0,1,0],
            [0,0,1,0,0,0,0,0,0,0,0,0, 1,1,0,1,1,1,0,0,0,1,0,1],
            [0,0,0,1,0,0,0,0,0,0,0,0, 1,0,1,1,1,0,0,0,1,0,1,1],
            [0,0,0,0,1,0,0,0,0,0,0,0, 1,1,1,1,0,0,0,1,0,1,1,0],
            [0,0,0,0,0,1,0,0,0,0,0,0, 1,1,1,0,0,0,1,0,1,1,0,1],
            [0,0,0,0,0,0,1,0,0,0,0,0, 1,1,0,0,0,1,0,1,1,0,1,1],
            [0,0,0,0,0,0,0,1,0,0,0,0, 1,0,0,0,1,0,1,1,0,1,1,1],
            [0,0,0,0,0,0,0,0,1,0,0,0, 1,0,0,1,0,1,1,0,1,1,1,0],
            [0,0,0,0,0,0,0,0,0,1,0,0, 1,0,1,0,1,1,0,1,1,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0, 1,1,0,1,1,0,1,1,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,1, 1,0,1,1,0,1,1,1,0,0,0,1],
        ]
        zn = 2
        word = read_one()
        encoded = encode_one(test_generator, word, zn)
        write_one(encoded)
    else:
        exit(1)