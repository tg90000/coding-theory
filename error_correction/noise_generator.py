import numpy as np
import textwrap
from typing import Callable
from random import random
import sys

def read_to_bin_str(path="./data/data.txt") -> str:
    ret = ""
    with open(path, "rb") as f:
        barray = f.read()
        ret = ''.join(format(byte, '08b') for byte in barray)
    return ret

def noise_fn(string: str, err_bits=1) -> str:
    err = 0
    string = list(string)
    for i in range(len(string)):
        if random() > .7:
            string[i] = str(1-int(string[i]))
            err += 1
            if err >= err_bits:
                break
    string = ''.join(string)
    return string

def add_noise(bin_str: str, data_word_len = 7, err_bits = 1) -> str:
    words = textwrap.wrap(bin_str, data_word_len)
    induced = map(noise_fn, words, [err_bits]*len(words))
    return ''.join(w for w in induced)

def write_file(bin_str: str, path="./data/data.txt"):
    barray = []
    chuncks = textwrap.wrap(bin_str, 8)
    with open(path, "wb") as binary_file:
        for chunck in chuncks:
            barray.extend(bytes([int(chunck, 2)]))
        binary_file.write(bytes(barray))
    return

def noise_fn_test(string: str, zn=2, err_bits=1) -> str:
    err = 0
    string = list(string)
    for i in range(len(string)):
        if random() > .7:
            string[i] = str(1-int(string[i]) % zn)
            err += 1
            if err >= err_bits:
                break
    string = ''.join(string)
    return string

def read_one(path="./data/data_one.txt")-> str:
    with open(path, "r") as f:
        data = f.readline()
        return data

def write_one(w: list[int], path="./data/data_one.txt") -> None:
    with open(path, "w") as f:
        string = "".join(str(c) for c in w)
        f.write(string)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        bin_data = read_to_bin_str()
        err_bin_text = add_noise(bin_data, 7, 1)
        write_file(err_bin_text)
    elif sys.argv[1] == "test1":
        codew = read_one()
        err_word = noise_fn_test(codew, zn=3, err_bits=1)
        write_one(err_word)
    elif sys.argv[1] == "test2":
        codew = read_one()
        err_word = noise_fn_test(codew, zn=2, err_bits=4)
        write_one(err_word)
    else:
        exit(1)