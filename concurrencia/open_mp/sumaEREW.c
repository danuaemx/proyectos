#include <omp.h>
#include <stdio.h>
#include <math.h>

int main(){
    printf("MODELO PRAM\n");
    printf("Suma EREW\n");
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
    float valores[n2];
    p = 1;
    for(i=0;i<n;++i){
        printf("Ingresa el elemento[%d]: ",i+1);
        scanf("%f",&valores[i]);
    }
    if(n != n2){
        for(i=n+1;i<n2;++i){
            valores[i]=0;
        }
    }
    for (i = 1; i <= exp; ++i){
        p = 2*p;
        printf("_____________________________\n");
        #pragma omp parallel
        {
            #pragma omp for
            for (j = 1; j <= n2/2; ++j)
            {
                if(2*j % p == 0){
                    //  se resta 1 ya que comienza en 0, p = 2**i
                    int idHilo = omp_get_thread_num();
                    printf("p_%d sumo [%d] y [%d] en el paso %d \n",idHilo,2*j,2*j-p/2,i);
                    valores[2*j-1] += valores[2*j-p/2-1];
                }
            }
        }

        printf("_____________________________\n");
    printf("[");
    for(int j=0; j<n2; ++j){
        printf("%.6f, ",valores[j]);
    }
    printf("]");
        
    }
    printf("_____________________________\n");
    printf("la suma es: ");
    printf("%.6f \n\n ",valores[n2-1]);

    printf("_____________________________\n");
    printf("[");
    for(i=0; i<n2; ++i){
        printf("%.6f, ",valores[i]);
    }
    printf("]");

    return 0;
}
