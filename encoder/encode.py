import math
import numpy


# ull fast_pow(ull a, ull m, ull p){
#     ull res = 1;
#     for (ull i = 0; (1 << i) <= m; i++){
#         if((m >> i) % 2 == 1) res = (res * a) % p;
#         a = ((a*a) % p);
#     }
#     return res;
# }

# a^e mod n
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
with open("../message.txt", "r") as f:
    text = f.read()
    nums = [int(word, 36) for word in text.split()]
    e=0
    n=0
    with open("./e_n.txt", "r") as keys:
        lines = [line[:-1] for line in keys.readlines()]
        e, n = [int(l) for l in lines]
    nums_coded = [fast_pow(num, e, n) for num in nums]
    encoded = [numpy.base_repr(num, 36) for num in nums_coded]
    str_encoded = ' '.join([str(elem) for elem in encoded])

with open("../message2.txt", "w") as f:
    f.write(str_encoded)


