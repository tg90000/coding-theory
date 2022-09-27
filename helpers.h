// fast_pow
//      bigmod
//      bigsquare
//      a pow x mod n
// euclidean
// diophantine
// primegen

#include <gmp.h>
#include <math.h>
#include <stdio.h>

#define ull unsigned long long 

ull square_mod(ull a, ull n){
    return ((a*a) % n);
}

// p-1 = 2^r * m
void find_m(ull p, ull *m, ull *r){
    *r =0;
    ull i=0;
    p--;
    while(p % (1 << ++i) == 0){}
    i--;
    *r = 1 << i;
    *m = p / *r;
}

// a^m mod p
ull fast_pow(ull a, ull m, ull p){
    ull res = 1;
    for (ull i = 0; (1 << i) <= m; i++){
        if((m >> i) % 2 == 1) res = (res * a) % p;
        a = ((a*a) % p);
    }
    return res;
}

// Miller-Rabin until a < 2*logn
int primecheck(ull p){
    if (p<3 || p%2==0)return 0;
    ull m,r;
    find_m(p, &m, &r);
    //printf("m: %llu, r: %llu\n", m, r);
    ull logp, var = p;
    for(logp = 0; var != 0; ++logp) var >>= 1; // get num of binary digits


    for (ull a = 2; a < 2*logp; a++){
        ull a_m = fast_pow(a, m, p);
        if (a_m == 1) continue;
        //printf("a: %llu, a_m: %llu\n", a, a_m);
        ull i_r = a_m; // (a^m)^(2^r)
        ull temp = 0;
        int ret = 0; // switch on -1s and 1s
        for (ull i = 0; i <= r; i++){
            if (i == r && i_r != 1) return 0; // a^(2^r * m) != 1 mod p
            if (i_r == p-1){ // a^(2^r * m) == -1 mod p
                if ((i_r * i_r) % p != 1) return 0; // a^(2^(r+1) * m) != 1 mod p
                else break;
            }
            i_r = (i_r * i_r) % p;
        }
    }
    return 1; // passes for each a
}


ull gcd(ull a, ull b){ // b > a
   if (b == 0) return a;
   return gcd(b, a % b);
}
