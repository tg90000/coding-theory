
import math
import numpy


def fast_pow(a, e, n):
    res = 1
    for i in range(e):
        if((e >> i) % 2 == 1): 
            res = (res * a) % n
        a = (a*a) % n
        if 1 << i > e:
            break
    return res

str_encoded = ""
with open("../message2.txt", "r") as f:
    text = f.read()
    nums = [int(word, 36) for word in text.split()]
    d=0
    n=0
    with open("./d_n.txt", "r") as keys:
        lines = [line[:-1] for line in keys.readlines()]
        d, n = [int(l) for l in lines]
    nums_coded = [fast_pow(num, d, n) for num in nums]
    encoded = [numpy.base_repr(num, 36) for num in nums_coded]
    str_encoded = ' '.join([str(elem) for elem in encoded])

with open("../message3.txt", "w") as f:
    f.write(str_encoded)