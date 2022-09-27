// fast_pow
//      bigmod
//      bigsquare
//      a pow x mod n
// euclidean
// diophantine
// ed fi(p)y = 1
// primegen

#include <gmp.h>
#include <math.h>
#include <stdio.h>

#define ull unsigned long long 
#define ll long long 

// p % a
ull bigmod(ull a, ull p){
    while(a<p)p-=a;
    return p;
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
    for(logp = 0; var != 0; ++logp) var >>= 1;      // get num of binary digits


    for (ull a = 2; a < 2*logp; a++){
        ull a_m = fast_pow(a, m, p); 
        if (a_m == 1) continue;
        //printf("a: %llu, a_m: %llu\n", a, a_m);
        ull i_r = a_m; 
        for (ull i = 0; i <= r; i++){               // (a^m)^(2^r)
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

ll gcd(ll a, ll b){
    return (b==0) ? a : gcd(b, a % b);
}

ll gcd_ext(ll a, ll b, ll *x, ll *y){
    if (b == 0) {
        *x = 1;
        *y = 0;
        return a;
    }else {
        ll g = gcd_ext(b, a % b, x, y);                 // basic rec. gcd
        ll x_prev = *x; 
        *x = *y;                                    // x = y
        *y = x_prev - (a / b) * (*y);               // y = gen
        return g;                                   // returns gcd, and preps x, y
    }
}

// returns x1 a solution, thats enough to generate d
ll diophantine_keygen(ll a, ll b, ll c){
    ll x, y;
    ll g = gcd_ext(a, b, &x, &y);                   // gonna be 1
    return ((x * c) + 2*b);                         // should be positive, adds as general solution
}





