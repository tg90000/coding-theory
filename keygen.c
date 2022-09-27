
// keygen: 
// input: p, q
// output: e, d, n

#include <stdio.h>
#include "helpers.h"
#define ull unsigned long long

int prime(ull p){
    for(ull i=2; i<p/2; i++){
        if (p%i==0)return 0;
    }
    return 1;
}

int main(){
    for (ull i = 999999800; i < 1000000000; i++){ // Miller-Rabin
        int pass = primecheck(i);
        if (pass)
            printf("%llu: %d\n", i, pass);
    }
    printf("DONE ===========================\n\n");

    for (ull i = 999999800; i < 1000000000; i++){ // Naive
        int pass = prime(i);
        if (pass)
            printf("%llu: %d\n", i, pass);
    }
    
    
    return 0;
}