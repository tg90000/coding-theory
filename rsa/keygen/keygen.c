#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include "helpers.h"
#define ull unsigned long long
#define ll long long
#define MINBITS 10
#define MINKEYLEN 10
#define MAXKEYLEN 20

// returns n
ull gen_keys(ull p, ull q, ull *e, ull *d){
    ull n = p*q;
    ull phi = (p-1) * (q-1);
    do{
        *e = rand() % (1 << MAXKEYLEN);
        if ((*e)<MINKEYLEN || (*e)%2==0)continue; // e > (1 << 20)
    }
    while(gcd(*e, phi) != 1);

    *d = diophantine_keygen(*e, phi, 1);

    return p*q;
}

ull gen_prime(){
    ull p = (1 << MINBITS) * (rand() % 128);
    do{
        p++;
    }
    while(!primecheck(p));

    return p;
}

int main(){
    srand(time(NULL));
    ull p = gen_prime();
    ull q = gen_prime();
    ull e, d, n;
    n = gen_keys(p, q, &e, &d);

    FILE* f_encode;
    f_encode = fopen("../encoder/e_n.txt", "w");
    fprintf(f_encode, "%llu\n%llu\n", e, n);
    fclose(f_encode);
    FILE* f_decode;
    f_decode = fopen("../decoder/d_n.txt", "w");
    fprintf(f_decode, "%llu\n%llu\n", d, n);
    fclose(f_decode);
    
    return 0;
}