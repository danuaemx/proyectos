#include <stdio.h>
#include<omp.h>

int main(){

    printf("MODELO PRAM\n");
    printf("Suma Busqueda y Ordenamiento CRCW\n");
    printf("_____________________________\n\n");
    //Rutina de ingreso de datos
    int n,i,j;
    printf("Ingresa el número de elementos: ");
    scanf("%d",&n);
    float valores[n];
    omp_set_num_threads(n*(n-1)/2);
    for(i=0;i<n;++i){
        printf("Ingresa el elemento[%d]: ",i+1);
        scanf("%f",&valores[i]);
    }
    int win[n], winh[n];
    float valoresOrd[n];

#pragma omp parallel for
    for(i = 0; i<n;++i){
        win[i]=0;
        winh[i]=0;
    }
const int T1 = n*(n-1)/2;
omp_set_num_threads(T1);
#pragma omp parallel for collapse(2) private(i,j) shared(win,winh)
    for(j=1;j<n;++j){
        for(i=0;i<j;++i){
            if(valores[i]>valores[j]){
                win[i]=1;
                winh[i]+=1;
                printf("p_%d encontró v[%d] > v[%d] \n",omp_get_thread_num(),i,j);
            }else{
                win[j]=1;
                winh[j]+=1;
                printf("p_%d encontró v[%d] < v[%d] \n",omp_get_thread_num(),i,j);
            }
        }
    }
#pragma omp parallel for
    for(i=0;i<n;++i){
        if (win[i]==0){
            printf("menor v[%d]  es %.6f \n",i,valores[i]);
        }
        valoresOrd[winh[i]]=valores[i];
    }

    printf("\n iteración %d: [",i);
    for (i = 0; i < n ; ++i){
        printf("%.6f, ",valoresOrd[i]);
    }
    printf("]\n");
    return 0;
}