#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc,char **argv) {
    long n = (argc>=2) ? atol(argv[1]) : 100000;
    char *out = (argc>=3) ? argv[2] : "out/in.bin";

    FILE *f=fopen(out,"wb"); if (!f) { perror("Arquivo de saída"); return 1; }
    
    srand(time(NULL));
    
    for(long i=0;i<n;i++) {
        int v = rand();
        fwrite(&v,sizeof(int),1,f);
    }
    
    fclose(f);
    printf("Arquivo '%s' gerado com %ld números aleatórios.\n", out, n);
    return 0;
}
