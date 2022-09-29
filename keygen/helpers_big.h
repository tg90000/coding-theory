#include <gmp.h>
#include <math.h>
#include <stdio.h>

#define ull unsigned long long 
#define ll long long 

// p-1 = 2^r * m, returns r
ull find_m(mpz_t p_i, mpz_t m){
    mpz_t p;
    mpz_init_set(p, p_i);
    ull r=0;
    mpz_sub_ui(p, p, 1);
    mpz_t rem;
    mpz_init(rem);

    while(mpz_cmp_ui(rem, 0)==0){
        r++;
        mpz_tdiv_r_2exp(rem, p, r);
    }
    r--;
    mpz_tdiv_q_2exp(m, p, r);                                   // set m to p / 2^r
    mpz_clear(p);
    mpz_clear(rem);
    return r;
}

// res = a^m mod p
void fast_pow(mpz_t a_i, mpz_t m_i, mpz_t p, mpz_t res){
    mpz_t a, m;
    mpz_init_set(a, a_i);
    mpz_init_set(m, m_i);
    mpz_init_set_d(res, 1);
    ull i = 0;
    while(mpz_cmp_ui(m, 0) > 0){ 
        if(mpz_fdiv_q_ui(m, m, 2) == 1){
            mpz_mul(res, res, a);
            mpz_mod(res, res, p);
        }
        mpz_mul(a, a, a);
        mpz_mod(a, a, p);
    }
    mpz_clear(a);
    mpz_clear(m);
}

// Miller-Rabin until a < 2*logn
int primecheck(mpz_t p){
    if (mpz_cmp_ui(p, 3) < 0 || mpz_even_p(p))return 0;

    mpz_t m;
    mpz_init(m);
    ull r;
    r = find_m(p, m);
    ull logp;
    mpz_t var;
    mpz_init_set(var, p);
    for(logp = 0; mpz_cmp_ui(var, 0) != 0; ++logp) mpz_fdiv_q_ui(var, var, 2);      // get num of binary digits

    mpz_t a_i, a_m, p_m1;
    mpz_init(p_m1);
    mpz_sub_ui(p_m1, p, 1);
    for (ull a = 2; a < 2*logp; a++){
        mpz_init_set_ui(a_i, a);
        mpz_init(a_m);
        fast_pow(a_i, m, p, a_m); 
        if (mpz_cmp_ui(a_m, 1)==0)continue;

        for (ull i = 0; i <= r; i++){                           // (a^m)^(2^r)
            if (i == r) {
                mpz_clear(m);
                mpz_clear(a_i);
                mpz_clear(a_m);
                mpz_clear(var);
                mpz_clear(p_m1);
                return 0;                                       // a^(2^r * m) != 1 mod p
            }
            if (mpz_cmp(a_m, p_m1)==0){                         // a^(2^r * m) == -1 mod p
                mpz_mul(a_m, a_m, a_m);
                mpz_mod(a_m, a_m, p);                           
                if (mpz_cmp_ui(a_m, 1)!=0) {
                    mpz_clear(m);
                    mpz_clear(a_i);
                    mpz_clear(a_m);
                    mpz_clear(var);
                    mpz_clear(p_m1);
                    return 0;                                   // a^(2^(r+1) * m) != 1 mod p
                }
                else break;
            }
            mpz_mul(a_m, a_m, a_m);
            mpz_mod(a_m, a_m, p);
        }
    }
    mpz_clear(m);
    mpz_clear(a_i);
    mpz_clear(a_m);
    mpz_clear(var);
    mpz_clear(p_m1);
    return 1;                                                   // passes for each a
}

// checks only for relative primes
int gcd(mpz_t a, mpz_t b){
    if (mpz_cmp_ui(b, 0) == 0) return mpz_cmp_ui(a, 1)==0 ? 1 : 0;
    mpz_t new_b;
    mpz_init(new_b);
    mpz_fdiv_r(new_b, a, b);                                    // new_b = a%b
    return gcd(b, new_b);
}

// returns 1 if gcd is 1
int gcd_ext(mpz_t a, mpz_t b, mpz_t x, mpz_t y){
    if (mpz_cmp_ui(b, 0) == 0) {
        mpz_set_ui(x, 1);
        mpz_set_ui(y, 0);
        return mpz_cmp_ui(a, 1)==0 ? 1 : 0;
    }else {
        mpz_t new_b;
        mpz_init(new_b);
        mpz_fdiv_r(new_b, a, b);                                // new_b = a%b
        int g = gcd_ext(b, new_b, x, y);                        // basic rec. gcd

        mpz_t x_prev;
        mpz_init_set(x_prev, x); 
        mpz_set(x, y);                                          // x = y

        mpz_t a_b;
        mpz_init(a_b);
        mpz_fdiv_q(a_b, a, b);
        mpz_mul(a_b, a_b, y);
        mpz_sub(y, x_prev, a_b);
        mpz_clear(a_b);
        mpz_clear(x_prev);
        return g;                                               // returns gcd, and preps x, y
    }
}

// returns x1 a solution, thats enough to generate d
int diophantine_keygen(mpz_t a, mpz_t b, mpz_t x1){ // c = 1
    mpz_t x, y;
    mpz_init(x);
    mpz_init(y);
    int g = gcd_ext(a, b, x, y);                                // gonna be 1   
    mpz_mul_ui(b, b, 2);
    mpz_add(x1, x, b);                                          // should be positive, adds as general solution
    mpz_clear(x);
    mpz_clear(y);
    return g;
}
