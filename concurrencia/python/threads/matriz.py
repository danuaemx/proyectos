import concurrent.futures
import math

global A,B,C

def leer_matriz(f):
    # Pedir al usuario el número de filas y columnas de la matriz
    filas = f
    # Crear una matriz vacía
    matriz = []

    # Pedir al usuario que ingrese los elementos de la matriz uno por uno
    print("Ingrese los elementos de la matriz, fila por fila:")
    for i in range(filas):
        fila = []
        for j in range(filas):
            elemento = float(input(f"Elemento en la posición ({i + 1}, {j + 1}): "))
            fila.append(elemento)
        matriz.append(fila)

    # Mostrar la matriz
    print("La matriz ingresada es:")
    for fila in matriz:
        print(fila)

    return matriz

def llenar(i,j,k):
    global A,B,C
    C[i][j][k]=A[i][k]*B[k][j]

def sumar(i,j,k,s):
    global C
    if((2*k)%pow(2,s)==0):
        C[i-1][j-1][2*k-1]+=C[i-1][j-1][2*k-int(pow(2,s-1))-1]



def main():
    global A,B,C
    f = int(input("Ingrese el número de filas/columnas de la matriz: "))
    A = leer_matriz(f)
    B = leer_matriz(f)
    C  = [[[0.0 for _ in range(f)] for _ in range(f)] for _ in range(f)]
    P = [(i,j,k) for i in range(0,f) for j in range(0,f) for k in range(0,f)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=f*f*f) as executor:
        executor.map(lambda pos: llenar(*pos), P)

        for s in range(0,int(math.log2(f))):
            P= [(i+1,j+1,k+1,s+1) for i in range(0,f) for j in range(0,f) for k in range(0,int(f/2))]
            executor.map(lambda pos: sumar(*pos), P)

    s = ''
    for m in range(0,f):
        s += '['
        for n in range (0,f):
            s = s + str(C[m][n][f-1])+', '
        s += ']\n'
    print(f'\n La matriz A*B es: \n {s}')



if __name__ == "__main__":
    main()
