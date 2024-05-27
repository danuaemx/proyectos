#include <omp.h>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int main(){
    int n,i,j,k,l,n2;
    omp_set_num_threads(3);
    printf("MODELO PRAM\n");
    printf("Multiplicación de Matrices\n");
    printf("_____________________________\n\n");

    //Rutina de ingreso de datos
    printf("Ingrese la potencia k, para 2^k filas y columnas de ambas matrices: ");
    scanf("%d",&n);
    n2 = (int)pow(2,n);

    double a[n2][n2];
    double b[n2][n2];
    double aux[n2][n2][n2];

    printf("Multiplicar dos matrices de %d x %d \n",n2,n2);

    //Ingresar A
    char s[100];
    printf("Ingresar A \n");
    for(i=0;i<n2;++i){
        for(j=0;j<n2;++j){
            printf("Ingresar A[%d][%d]: ",i+1,j+1);
            scanf("%s",&s);
            a[i][j]= strtod(s,NULL);

        }
    }
    printf("\n");
    
    //Ingresar B
    printf("Ingresar B: \n");
    for(i=0;i<n2;++i){
        for(j=0;j<n2;++j){
            printf("Ingresar B[%d][%d]: ",i+1,j+1);
            scanf("%s",&s);
            b[i][j]= strtod(s,NULL);
        }
    }
    //Imprimir A
    printf("A ingresada como \n\n");
    for(i=0;i<n2;++i){
        printf("[ ");
        for(j=0;j<n2;++j){
            printf("%.6f,\t ",a[i][j]);
        }
        printf("] \n\n");
    }
    //Imprimir B
    printf("B ingresada como \n\n");
    for(i=0;i<n2;++i){
        printf("[ ");
        for(j=0;j<n2;++j){
            printf("%.6f,\t",b[i][j]);
        }
        printf("] \n\n");
    }
    const int T1 = n2*n2*n2;
    printf("%d hilos en paso 1 \n",T1);
    omp_set_num_threads(T1);
    #pragma omp parallel for collapse(3) private (i,j,k) shared(a,b,aux)
    for (i=0;i<n2;++i){
        for(j=0;j<n2;++j){
            for(k=0;k<n2;++k){
                 aux[i][j][k]=a[i][k]*b[k][j];
                 printf("p_%d calculo (%d,%d,%d) en paso #1 \n",omp_get_thread_num(),i,j,k);
            }
        }
    }
    const int T2 = n2*n2*n2/2;
    printf("%d hilos en paso 2 \n",T2);
    omp_set_num_threads(T2);
    for(l=1;l<=n;++l){
       #pragma omp parallel for collapse(3) private (i,j,k) shared (aux,l)
       for (i=1;i<=n2;++i){
            for(j=1;j<=n2;++j){
                for(k=1;k<=(int)(n2/2);++k){
                    if((2*k)%(int)pow(2,l)==0){
                        aux[i-1][j-1][2*k-1]+=aux[i-1][j-1][2*k-(int)pow(2,l-1)-1];
                        printf("p_%d calculo (%d,%d,%d) en paso #2.%d \n",omp_get_thread_num(),i,j,2*k,l);
                    }
                }
            }
        }
    }

    //Resultante Imprimir
    printf("\n La matriz A*B es: \n");
    for(i=0;i<n2;++i){
        printf("[ ");
        for(j=0;j<n2;++j){
            printf("%.6f,\t",aux[i][j][n2-1]);
        }
        printf("] \n");
    }

    return 0;
}