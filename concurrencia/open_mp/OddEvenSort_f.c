#include <stdio.h>
#include <omp.h>
#include <math.h>
#include <stdlib.h>


void printArr(double aux[], const int p_i, const int l) {
    printf("\n [");
    for (int i = 0; i < l; ++i) {
        int p = i + p_i;
        printf("%.6f, ", aux[p]);
    }
    printf("]");
}

void oddEvenSplit(double aux[], double odd[],double even[], const int m) {
#pragma omp parallel for
    for(int i=0; i<m;++i) {
        //printf("\n \t \t %d proceso oems split paralelo", omp_get_thread_num());
        odd[i]= aux[2*i+1];
        even[i]= aux[2*i];
    }
}

void oddEvenMerge(double aux[], const int l) {
    if (l == 2) {
        //printf("\n ______________________________________________");
        //printf("\n \t %d proceso oem n==2 oems with i= %d n= %d", omp_get_thread_num(), p_i, l);
        if (aux[0] > aux[1]) {
            const double tmp = aux[0];
            aux[0] = aux[1];
            aux[1] = tmp;
        }
    } else {
        int m = l / 2;
            double odd[m];
            double even[m];
            //OddEvenSplit
                //printf("\n ______________________________________________");
                //printf("\n \t %d proceso SPLIT i= %d n= %d", omp_get_thread_num(), p_i, l);
#pragma omp task  shared(aux,odd,even)
            oddEvenSplit(aux,odd,even,m);

            //Llamada recursiva a odd e even
#pragma omp taskwait
        //printf("\n ______________________________________________");
#pragma omp task  shared(odd)

            //printf("\n \t %d proceso oem ODD i= %d n= %d", omp_get_thread_num(), p_i, l);
            oddEvenMerge(odd,m);

#pragma omp task  shared(even)

            //printf("\n \t %d proceso oem EVEN i= %d n= %d", omp_get_thread_num(), p_i, l);
            oddEvenMerge(even,m);

#pragma omp taskwait
            //une los dos
            //printf("\n ______________________________________________");
            //printf("\n \t %d proceso oem Unir i= %d n= %d", omp_get_thread_num(), p_i, l);
            int i;
#pragma omp parallel for private(i)
            for(i=0; i<m;++i) {
                //printf("\n \t \t  %d proceso oems unión paralela", omp_get_thread_num());
                aux[2*i+1]=odd[i];
                aux[2*i]=even[i];
            }
#pragma omp taskwait

            //printf("\n ______________________________________________");
            //printf("\n \t %d proceso oem COMPARACIÓN i= %d n= %d", omp_get_thread_num(), p_i, l);
            //Compara
#pragma omp parallel for
            for (int i = 1; i < m; ++i) {
                //printf("\n \t \t %d proceso oems comparación paralela", omp_get_thread_num());
                if (aux[2 * i -1] > aux[2 * i ]) {
                    const double tmp = aux[2 * i -1];
                    aux[2 * i -1] = aux[2 * i ];
                    aux[2 * i ] = tmp;
                }
            }
    }
}

void oddEvenMergeSort(double aux[], const int l) {
    if (l > 1) {
        const int m = l / 2;
#pragma omp task shared(aux)
        {
            oddEvenMergeSort(aux,m);
            //printf("\n %d proceso oems izquierdo i= %d n= %d", omp_get_thread_num(), p_i, m);
        }
#pragma omp task shared(aux)
        {
            oddEvenMergeSort(aux+m, m);
            //printf("\n %d proceso oems derecho i= %d n= %d", omp_get_thread_num(), p_i + m, l - m);
        }
#pragma omp taskwait
        {
            //printf("\n ______________________________________________");
            //printf("\n llamada a oem");
            oddEvenMerge(aux,l);
        }
    }
}

int main(){
    int i;
    int n1;
    printf("MODELO PRAM\n");
    printf("Odd Even Sort\n");
    printf("_____________________________\n\n");

    //Rutina de ingreso de datos
    printf("Ingrese la potencia k, para 2^k renglones de 1 a 10: ");
    scanf("%d",&n1);
    const int n2 = (int)pow(2,n1);
    printf("Ordenar vector de %d\n",n2);
    double L[n2];
    //Ingresar
    printf("Ingresar V \n");
    char *s = malloc(100*sizeof(char));
    for(i=0;i<n2;++i){
        printf("Ingresar V[%d]: ",(i+1));
        scanf("%s",s);
        L[i] = strtod(s,NULL);
    }
    printf("\n");
    //Asegura que los threds sean n
    omp_set_num_threads(n2);
    //Garantiza la ejecución de regiones paralelas dentro de otras
omp_set_nested(1);
    const double start_time = omp_get_wtime();
#pragma omp parallel shared(L,n2)
    {
#pragma omp single
        {
            oddEvenMergeSort(L,n2);
        }
    }
    const double end_time = omp_get_wtime();
    printf("\n \n Tiempo de ejecución: %f segundos\n", end_time - start_time);
    //Regresar valor;
    printf("\n El vector resulante \n");
    printArr(L,0,n2);
    printf("\n");


    return 0;
}



