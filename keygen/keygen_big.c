#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <gmp.h>
#include "helpers_big.h"
#define ull unsigned long long
#define ll long long
#define MINBITS 500
#define MAXBITS 512
#define MINKEYLEN 500
#define MAXKEYLEN 512
#define SEED 8192

// returns n
void gen_keys(mpz_t p, mpz_t q, mpz_t e, mpz_t d, mpz_t n){
    mpz_mul(n, p, q);
    mpz_t phi;
    mpz_init(phi);
    mpz_sub(phi, n, p);
    mpz_sub(phi, phi, q);
    mpz_sub_ui(phi, phi, 1);                            // (p-1)*(q-1) = n - p - q + 1

    mpz_t e_gcd;
    mpz_init_set_ui(e_gcd,1);
    mpz_t phi_gcd;
    mpz_init_set(phi_gcd, phi); 

    gmp_randstate_t rstate;
    gmp_randinit_mt(rstate);
    ull seed = (1 << 24) * (rand() % SEED);
    gmp_randseed_ui(rstate, seed);
    mpz_t min;
    mpz_init(min);
    mpz_ui_pow_ui(min, 2, MINKEYLEN);
    mpz_urandomb(e, rstate, MAXKEYLEN);
    mpz_add(e, e, min);
    if (mpz_even_p(e)) mpz_add_ui(e, e, 1);
    int x = 0;
    do{
        mpz_add_ui(e, e, 2);
        mpz_set(e_gcd, e);
        mpz_set(phi_gcd, phi);
    }while(gcd(e_gcd, phi_gcd) != 1);

    mpz_set(e_gcd, e);
    mpz_set(phi_gcd, phi);
    diophantine_keygen(e_gcd, phi_gcd, d);
    gmp_randclear(rstate);
    mpz_clears(phi, e_gcd, phi_gcd, min);
}

// returns p
void gen_prime(mpz_t p){
    ull seed = (1 << 24) * (rand() % SEED);
    gmp_randstate_t rstate;
    gmp_randinit_mt(rstate);
    gmp_randseed_ui(rstate, seed);
    mpz_t min;
    mpz_init(min);
    mpz_ui_pow_ui(min, 2, MINBITS);
    mpz_urandomb(p, rstate, MAXBITS);
    mpz_add(p, p, min);
    if (mpz_even_p(p)){mpz_add_ui(p, p, 1);}
    do {
        mpz_add_ui(p, p, 2);
    } while (!primecheck(p)); 
    gmp_randclear(rstate);
    mpz_clear(min);
}

int main(){
    srand(time(NULL));
    mpz_t p, q, e, d, n;
    mpz_init(p);
    mpz_init(q);
    mpz_init(e);
    mpz_init(d);
    mpz_init(n);
    gen_prime(p);
    gen_prime(q);
    gen_keys(p, q, e, d, n);

    FILE* f_encode;
    f_encode = fopen("../encoder/e_n.txt", "w");
    mpz_out_str(f_encode, 10, e);
    fprintf(f_encode, "\n");
    mpz_out_str(f_encode, 10, n);
    fclose(f_encode);
    FILE* f_decode;
    f_decode = fopen("../decoder/d_n.txt", "w");
    mpz_out_str(f_decode, 10, d);
    fprintf(f_decode, "\n");
    mpz_out_str(f_decode, 10, n);
    fclose(f_decode);
    
    return 0;
}