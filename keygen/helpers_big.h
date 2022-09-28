#include <gmp.h>
#include <math.h>
#include <stdio.h>

#define ull unsigned long long 
#define ll long long 

// p % a
void bigmod(mpz_t a_i, mpz_t p_i, mpz_t res){
    mpz_t a, p;
    mpz_init(a);
    mpz_init(p);
    mpz_set(a, a_i);
    mpz_set(p, p_i);
    while(mpz_cmp(a,p) < 0){mpz_sub(p, p, a);}
    mpz_set(res, p);
}

// p-1 = 2^r * m
void find_m(mpz_t p_i, mpz_t m, mpz_t r){
    mpz_t p;
    mpz_init_set(p, p_i);
    mpz_init_set_d(r, 1);
    ull i=0;
    mpz_sub_ui(p, p, 1);
    mpz_t rem;
    mpz_init(rem);

    while(mpz_cmp_ui(rem, 0)){
        i++;
        mpz_tdiv_r_2exp(rem, p, i);
    }
    i--;
    mpz_mul_2exp(r, r, i);
    mpz_fdiv_q(m, p, r);
}

// res = a^m mod p
mpz_t fast_pow(mpz_t a, mpz_t m, mpz_t p, mpz_t res){
    mpz_t res = 1;
    for (mpz_t i = 0; (1 << i) <= m; i++){
        if((m >> i) % 2 == 1) res = (res * a) % p;
        a = ((a*a) % p);
    }
    return res;
}

// Miller-Rabin until a < 2*logn
int primecheck(mpz_t p){
    if (p<3 || p%2==0)return 0;
    mpz_t m,r;
    find_m(p, &m, &r);
    //printf("m: %llu, r: %llu\n", m, r);
    mpz_t logp, var = p;
    for(logp = 0; var != 0; ++logp) var >>= 1;      // get num of binary digits


    for (mpz_t a = 2; a < 2*logp; a++){
        mpz_t a_m = fast_pow(a, m, p); 
        if (a_m == 1) continue;
        //printf("a: %llu, a_m: %llu\n", a, a_m);
        mpz_t i_r = a_m; 
        for (mpz_t i = 0; i <= r; i++){               // (a^m)^(2^r)
            if (i == r && a_m != 1) return 0;       // a^(2^r * m) != 1 mod p
            if (a_m == p-1){                        // a^(2^r * m) == -1 mod p
                if ((a_m * a_m) % p != 1) return 0; // a^(2^(r+1) * m) != 1 mod p
                else break;
            }
            a_m = (a_m * a_m) % p;
        }
    }
    return 1; // passes for each a
}

mpz_t gcd(mpz_t a, mpz_t b){
    return (b==0) ? a : gcd(b, a % b);
}

mpz_t gcd_ext(mpz_t a, mpz_t b, mpz_t *x, mpz_t *y){
    if (b == 0) {
        *x = 1;
        *y = 0;
        return a;
    }else {
        mpz_t g = gcd_ext(b, a % b, x, y);             // basic rec. gcd
        mpz_t x_prev = *x; 
        *x = *y;                                    // x = y
        *y = x_prev - (a / b) * (*y);               // y = gen
        return g;                                   // returns gcd, and preps x, y
    }
}

// returns x1 a solution, thats enough to generate d
mpz_t diophantine_keygen(mpz_t a, mpz_t b, mpz_t c){
    mpz_t x, y;
    mpz_t g = gcd_ext(a, b, &x, &y);                   // gonna be 1
    return ((x * c) + 2*b);                         // should be positive, adds as general solution
}
