#include <stdio.h>
#include<omp.h>
#include<math.h>

int main(){
 
    printf("MODELO PRAM\n");
    printf("Suma CREW\n");
    printf("_____________________________\n\n");
    //Rutina de ingreso de datos
    int n,i,j,p,n2,exp;
    printf("Ingresa el número de elementos(mejor si es potencia de 2): ");
    scanf("%d",&n);
    exp = (int)(floor(log2(n))+1);
    n2 = (int)pow(2,exp);
    if(2*n==n2){
        n2 = n;
        exp = exp-1;
    }
    double valores[n2],valAux[n2];
    p = 1;
    for(i=0;i<n;++i){
        printf("Ingresa el elemento[%d]: ",i+1);
        scanf("%lf",&valores[i]);
        valAux[i]=valores[i];
    }
    if(n != n2){
        for(i=n+1;i<n2;++i){
            valores[i]=0;
            valAux[i]=0;
        }
    }


    printf("\n Original: [");
        for (int i = 0; i < n; ++i){
            printf("%.6f, ",valores[i]);
        }
    printf("]\n");

    for (int i = 1; i <= exp; ++i){
        p = p*2;
        printf("_____________________________\n");
        #pragma omp parallel
        {
            #pragma omp for
            for (int j = p/2+1 ; j <= n2; ++j){
                //  se resta 1 ya que comienza en 0, p = 2**i
                //  se resta 1 ya que comienza en 0, p = 2**i
                int idHilo = omp_get_thread_num();
                printf("p_%d sumo [%d] y [%d] en el paso %d \n",idHilo,j,j-p/2,i);
                valores[j-1] += valAux[j-p/2-1];
                }

            #pragma omp for
            for (int j = p/2+1 ; j <= n2; ++j){
                valAux[j-1] = valores[j-1];
            }
        }
        printf("\n iteración %d: [",i);
        for (int i = 0; i < n; ++i){
            printf("%.6f, ",valores[i]);
        }
        printf("]\n");

    }
    return 0;
}