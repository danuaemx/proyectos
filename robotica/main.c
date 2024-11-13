#include <stdio.h>
#include <math.h>

#define L1 10.0
#define L2 8.0
#define RAD_DEG (180/M_PI)

void calcular_natural(double x, double y, double *m_Hip, double *phi){
    double l3 = sqrt(pow(x, 2) + pow(y, 2));
    double theta = atan2(y, x);
    double cos_Phi = (pow(l3, 2) - pow(L1, 2) - pow(L2, 2)) / (2 * L1 * L2);
    *phi = acos(cos_Phi);
    double sin_Phi = sin(*phi);
    double zeta = atan2(L2 * sin_Phi, L1 + L2 * cos_Phi);
    *m_Hip = 180 + (theta - zeta) * RAD_DEG;
    *phi *= RAD_DEG;
}
void calcular_adicional(double x, double y, double *m_Hip, double *phi){
    double l3 = sqrt(pow(x, 2) + pow(y, 2));
    double theta = atan2(y, x);
    double cos_Phi = (pow(l3, 2) - pow(L1, 2) - pow(L2, 2)) / (2 * L1 * L2);
    *phi = acos(cos_Phi);
    double sin_Phi = sin(*phi);
    double zeta = atan2(L2 * sin_Phi, L1 + L2 * cos_Phi);
    //Cambiar formulas para segunda solución
    *m_Hip = 180 + (theta + zeta) * RAD_DEG;
    *phi *= -1*RAD_DEG;
}

int main(){
    double x, y;
    double qhip, qknee;
    double qhip_1, qknee_1;
    
    // Solicitar las coordenadas X e Y
    printf("Introduce la coordenada X: ");
    scanf("%lf", &x);
    
    printf("Introduce la coordenada Y: ");
    scanf("%lf", &y);

    // Calcular los ángulos de la cadera y la rodilla
    calcular_natural(x, y, &qhip, &qknee);
    calcular_adicional(x,y,&qhip_1, &qknee_1);
    
    // Imprimir los resultados
    printf("El ángulo de la cadera (qHip) es: %.2f grados a partir de Rot(z,180)\n", qhip);
    printf("El ángulo de la rodilla (qKnee) es: %.2f grados\n", qknee);
    printf("El ángulo de la cadera extra (qHip) es: %.2f grados a partir de Rot(z,180)\n", qhip_1);
    printf("El ángulo de la rodilla extra (qKnee) es: %.2f grados\n", qknee_1);
    
    return 0;
}
