import numpy as np
import textwrap
from typing import Callable
from random import random

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

bin_data = read_to_bin_str()
err_bin_text = add_noise(bin_data, 7, 1)
write_file(err_bin_text)