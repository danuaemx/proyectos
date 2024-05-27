#include <omp.h>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#define MAX 134217728


double a[MAX];
int n2 = MAX;
int n = MAX;
int id = 0;

void inter(int i, int j){
    double t=a[i];
    a[i]=a[j];
    a[j]=t;
}

void compara(int i, int j){
    if (a[i]>a[j])
    inter(i, j);
}

void oddEvenMerge(int p_i, int n, int des){
    ++id;
    int des2=des*2;
    if (des2<n){
        #pragma omp nowait task 
        {
        //printf("p_%d llamada paralela OddEven en sublista Even, id%d \n",omp_get_thread_num(),id);
        oddEvenMerge(p_i, n, des2);

        }
        #pragma omp nowait task
        {
        //printf("p_%d llamada parallela OddEven caso sublista Odd, id%d  \n",omp_get_thread_num(),id);
        oddEvenMerge(p_i+des, n, des2);
        }
        #pragma omp for
            for (int i=p_i; i<p_i+n-des2; i+=des2){
                //printf("\t p_%d Comparo en caso en OddEven [%d] con [%d], id%d  \n",omp_get_thread_num(),i+1,i+des+1,id);
                compara(i+des, i+des2);
            }
        }else{
            //printf("\t p_%d Caso base OddEven comparo [%d] con [%d], id%d  \n",omp_get_thread_num(),p_i+1,p_i+des+1,id);
            compara(p_i, p_i+des);
        }
}


void oddEvenMergeSort(int p_0, int n){
    if (n>1){
        ++id;
        int m=n/2;
        #pragma omp nowait task
        {
        //printf("p_%d llamada paralela Merge en Merge, id%d  \n",omp_get_thread_num(),id);
        oddEvenMergeSort(p_0, m);
        }
        #pragma omp nowait task
        {
        //printf("p_%d llamada paralela a Merge en Merge, id%d  \n",omp_get_thread_num(),id);
        oddEvenMergeSort(p_0+m, m);
        }
        #pragma omp nowait task
        //printf("p_%d llamada a OddEven en Merge, id%d  \n",omp_get_thread_num(),id);
        oddEvenMerge(p_0, n, 1);
    }
}



int main(){
    int i;

    printf("MODELO PRAM\n");
    printf("Odd Even Sort\n");
    printf("_____________________________\n\n");

    //Rutina de ingreso de datos
    printf("Ingrese la potencia k, para 2^k renglones de 1 a 27: ");
    scanf("%d",&n);
    n2 = (int)pow(2,n);
    printf("Ordenar vector de %d\n",n2);

    //Ingresar
    printf("Ingresar V \n");
    char *s = malloc(100*sizeof(char));
    for(i=0;i<n2;++i){
        printf("Ingresar V[%d]: ",(i+1));
        scanf("%s",s);
        a[i] = strtod(s,NULL);
    }
    printf("\n");
    //Asegura que los threds sean n
    omp_set_num_threads(n2*n2);
    const double start_time = omp_get_wtime();
    #pragma omp parallel
    {
        #pragma omp nowait single
        {
            oddEvenMergeSort(0,n2);
        }
    
    }
    const double end_time = omp_get_wtime();
    //Regresar valor;
    printf("\n \n Tiempo de ejecución: %f segundos\n", end_time - start_time);

    printf("El vector resulante \n [,");
    for (i = 0; i < n2 ; ++i){
        printf("%.6f, ",a[i]);
    }
    printf("]\n");



    return 0;
}