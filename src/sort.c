#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void merge(int *a, int l, int m, int r) {
    int i, j, k, n1 = m - l + 1, n2 = r - m;
    int *L = malloc(n1 * sizeof(int)), *R = malloc(n2 * sizeof(int));
    for (i = 0; i < n1; i++) L[i] = a[l + i];
    for (j = 0; j < n2; j++) R[j] = a[m + 1 + j];
    i = 0; j = 0; k = l;
    while (i < n1 && j < n2) a[k++] = (L[i] <= R[j]) ? L[i++] : R[j++];
    while (i < n1) a[k++] = L[i++];
    while (j < n2) a[k++] = R[j++];
    free(L); free(R);
}

void mergesort(int *a, int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
        mergesort(a, l, m);
        mergesort(a, m + 1, r);
        merge(a, l, m, r);
    }
}

int partition(int *a, int l, int r) {
    int p = a[r], i = l - 1, t;
    for (int j = l; j < r; j++)
        if (a[j] <= p) { i++; t = a[i]; a[i] = a[j]; a[j] = t; }
    t = a[i + 1]; a[i + 1] = a[r]; a[r] = t;
    return i + 1;
}
void quicksort(int *a, int l, int r) {
    if (l < r) {
        int pi = partition(a, l, r);
        quicksort(a, l, pi - 1);
        quicksort(a, pi + 1, r);
    }
}

void print_usage(char *progname) {
    printf("Uso: %s [merge|quick] [arquivo_entrada] [arquivo_saida]\n", progname);
}

int main(int argc, char **argv) {
    char *alg = "merge", *infile = "out/in.bin", *outfile = "out/out.bin";
    if (argc >= 2) alg = argv[1];
    if (argc >= 3) infile = argv[2];
    if (argc >= 4) outfile = argv[3];

    if (strcmp(alg, "merge") != 0 && strcmp(alg, "quick") != 0) {
        printf("Algoritmo inválido: use 'merge' ou 'quick'.\n");
        print_usage(argv[0]);
        return 1;
    }

    FILE *f = fopen(infile, "rb");
    if (!f) { perror("Arquivo de entrada"); return 1; }
    fseek(f, 0, SEEK_END); long n = ftell(f) / sizeof(int);
    rewind(f);
    
    int *a = malloc(n * sizeof(int));
    fread(a, sizeof(int), n, f); fclose(f);

    if (strcmp(alg, "merge") == 0) {
        mergesort(a, 0, n - 1);
    } else {
        quicksort(a, 0, n - 1);
    }

    f = fopen(outfile, "wb");
    if (!f) { perror("Arquivo de saída"); free(a); return 1; }
    fwrite(a, sizeof(int), n, f); fclose(f);
    free(a);

    printf("Ordenação sequencial completa com algoritmo %s (%ld elementos)\n", alg, n);
    return 0;


}
