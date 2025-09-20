#include <stdio.h>
#include <stdlib.h>

int main(int argc,char **argv) {
    char *infile = (argc>=2)?argv[1]:"out/out.bin";
    FILE *f=fopen(infile,"rb");

    if (!f) { perror("Arquivo de entrada"); return 1; }
    
    int prev, curr, idx=0;
    
    if (fread(&prev, sizeof(int), 1, f) != 1) {
        printf("Arquivo vazio.\n");
        fclose(f); return 0;
    }
    
    while (fread(&curr,sizeof(int),1,f)==1) {
        idx++;
        if (curr<prev) {
            printf("Erro: não ordenado na posição %d (%d>%d)\n", idx, prev, curr);
            fclose(f); return 1;
        }
        prev=curr;
    }
    
    fclose(f);
    printf("Arquivo '%s' está ordenado corretamente (%d elementos verificados).\n", infile, idx+1);
    return 0;
}
