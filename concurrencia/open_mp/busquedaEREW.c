#include <stdio.h>
#include<omp.h>
#include<math.h>

int main() {
    int s;
    printf("MODELO PRAM\n");
    printf("Busqueda EREW\n");
    printf("_____________________________\n\n");
    //Rutina de ingreso de datos
    int n, i, j, p, n2, exp;
    float x;
    printf("Ingresa el número de elementos(mejor si es potencia de 2): ");
    scanf("%d", &n);
    exp = (int) (floor(log2(n)) + 1);
    n2 = (int) pow(2, exp);
    if (2 * n == n2) {
        n2 = n;
        exp = exp - 1;
    }
    float valores[n2];
    float aux[n2];

    for (i = 0; i < n; ++i) {
        printf("Ingresa el elemento[%d]: ", i + 1);
        scanf("%f", &valores[i]);
    }
    if (n != n2) {
        for (i = n + 1; i < n2; ++i) {
            valores[i] = 0;
        }
    }

    printf("Ingresa el número a buscar: ");
    scanf("%f", &x);
    p = 1;
    aux[0] = x;
    //Broadcast
    for (i = 1; i <= exp; ++i) {
        p = 2 * p;
#pragma omp parallel for private(j) shared(aux)
        for (j = (int) (p / 2 + 1); j <= p; ++j) {
            aux[j - 1] = aux[j - p / 2 - 1];
            printf("p_%d asingo x de aux[%d] a aux[%d] en el paso [%d] \n", omp_get_thread_num(), j - p / 2, j, i);
        }
    }
    //Ordenamiento

#pragma omp parallel for private(i) shared(aux,valores)
    for (i = 0; i < n2; ++i) {
        if (valores[i] != aux[i]) {
            aux[i] = 1000000000.0;
            printf("p_%d asingo Infinito en aux[%d] \n", omp_get_thread_num(), i);
        }
    }

    //Minimo
    p = 1;
    for (j = 0; j < exp; ++j) {
        p = 2 * p;
#pragma omp parallel for private(i) shared(aux)
        for (i = 1; i <= n2 / p; ++i) {
            int inf = 2 * i - 1;
            int sup = 2 * i;
            if ((aux[inf - 1] != 1000000000.0) | (aux[sup - 1] != 1000000000.0)) {
                if (aux[inf - 1] > aux[sup - 1]) {
                    aux[i - 1] = aux[sup - 1];
                    printf("p_%d asingo aux[%d] en aux[%d] en paso %d \n", omp_get_thread_num(), sup, i, j);
                } else {
                    aux[i - 1] = aux[inf - 1];
                    printf("p_%d asingo aux[%d] en aux[%d] paso %d \n", omp_get_thread_num(), inf, i, j);
                }
            }
            printf("p_%d encontró par infinito en[%d,%d] paso %d \n", omp_get_thread_num(), inf, sup, j);
        }
    }

    //Regresar valor;
    printf("El vector resulante \n [,");
    for (i = 0; i < n; ++i) {
        if (aux[i] != 1000000000.0) {
            printf("%.6f, ", aux[i]);
            s = i+1;
        } else {
            printf("Infinito, ");
        }
    }
    printf("]\n");

    printf("El resultado de la busqueda es: ");
    if (aux[0] == x) {
        printf("Encontrado en %d \n", s);
    } else {
        printf("No existe \n");
    }
}
