
// keygen: 
// input: p, q
// output: e, d, n

#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include "helpers.h"
#define ull unsigned long long
#define ll long long
#define MINBITS 20
#define MINKEYLEN 3

// returns n
ull gen_keys(ull p, ull q, ull *e, ull *d){
    ull n = p*q;
    ull phi = (p-1) * (q-1);
    
    do{
        *e = rand()*rand()-1;
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
    // for (ull i = 999999800; i < 1000000000; i++){ // Miller-Rabin
    //     int pass = primecheck(i);
    //     if (pass)
    //         printf("%llu: %d\n", i, pass);
    // }
    // printf("DONE ===========================\n\n");

    // ull res;
    // res = bigmod(7, 88);
    // printf("%llu\n", res);

    // ll d;
    // d = diophantine_keygen(7, 5, 1);
    // printf("%lld\n", d);

    // ll g = gcd(9, 24);
    // printf("%lld\n", g);

    // ull p;
    // p = gen_prime();
    // printf("%lld\n", p);


    
    return 0;
}