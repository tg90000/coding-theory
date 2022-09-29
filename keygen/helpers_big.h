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
    mpz_tdiv_q_2exp(m, p, r); // set m to p / 2^r
    return r;
}

// res = a^m mod p
void fast_pow(mpz_t a_i, mpz_t m_i, mpz_t p, mpz_t res){
    mpz_t a, m;
    mpz_init_set(a, a_i);
    mpz_init_set(m, m_i);
    mpz_init_set_d(res, 1);
    ull i = 0;
    mpz_t n2exp;
    mpz_init_set_ui(n2exp, 1);
    while(mpz_cmp_ui(m, 0) > 0){ //(1 << i) <= m
        if(mpz_fdiv_q_ui(m, m, 2) == 1){
            mpz_mul(res, res, a);
            mpz_mod(res, res, p);
        }
        mpz_mul(a, a, a);
        mpz_mod(a, a, p);
    }
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
    printf("logp: %llu\n============================\n", logp);

    mpz_t a_i, a_m, p_m1;
    mpz_init(p_m1);
    mpz_sub_ui(p_m1, p, 1);
    for (ull a = 2; a < 2*logp; a++){
        mpz_init_set_ui(a_i, a);
        mpz_init(a_m);
        fast_pow(a_i, m, p, a_m); 
        if (mpz_cmp_ui(a_m, 1)==0)continue;

        for (ull i = 0; i <= r; i++){               // (a^m)^(2^r)
            if (i == r) return 0;                   // a^(2^r * m) != 1 mod p
            if (mpz_cmp(a_m, p_m1)==0){                        // a^(2^r * m) == -1 mod p
                mpz_mul(a_m, a_m, a_m);
                mpz_mod(a_m, a_m, p);                           
                if (mpz_cmp_ui(a_m, 1)!=0) return 0;             // a^(2^(r+1) * m) != 1 mod p
                else break;
            }
            mpz_mul(a_m, a_m, a_m);
            mpz_mod(a_m, a_m, p);
        }
    }
    return 1; // passes for each a
}

// mpz_t gcd(mpz_t a, mpz_t b){
//     return (b==0) ? a : gcd(b, a % b);
// }

// mpz_t gcd_ext(mpz_t a, mpz_t b, mpz_t *x, mpz_t *y){
//     if (b == 0) {
//         *x = 1;
//         *y = 0;
//         return a;
//     }else {
//         mpz_t g = gcd_ext(b, a % b, x, y);             // basic rec. gcd
//         mpz_t x_prev = *x; 
//         *x = *y;                                    // x = y
//         *y = x_prev - (a / b) * (*y);               // y = gen
//         return g;                                   // returns gcd, and preps x, y
//     }
// }

// // returns x1 a solution, thats enough to generate d
// mpz_t diophantine_keygen(mpz_t a, mpz_t b, mpz_t c){
//     mpz_t x, y;
//     mpz_t g = gcd_ext(a, b, &x, &y);                   // gonna be 1
//     return ((x * c) + 2*b);                         // should be positive, adds as general solution
// }
