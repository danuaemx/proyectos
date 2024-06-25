import math
import multiprocessing as mp


def leer_matriz(f, manager):

    # Pedir al usuario el número de filas y columnas de la matriz
    filas = f
    # Crear una matriz vacía
    matriz = manager.list()  # Crear una lista de multiprocessing

    # Pedir al usuario que ingrese los elementos de la matriz uno por uno
    print("Ingrese los elementos de la matriz, fila por fila:")
    for i in range(filas):
        fila = manager.list()  # Crear una lista de multiprocessing
        for j in range(filas):
            elemento = float(input(f"Elemento en la posición ({i + 1}, {j + 1}): "))
            fila.append(elemento)
        matriz.append(fila)

    print("La matriz ingresada es:")
    for fila in matriz:
        print(fila)

    return matriz

def llenar(A,B,C,i,j,k):
    C[i][j][k]=A[i][k]*B[k][j]

def sumar(C,i,j,k,s):
    if((2*k)%pow(2,s)==0):
        C[i-1][j-1][2*k-1]+=C[i-1][j-1][2*k-int(pow(2,s-1))-1]



def main():
    with mp.Manager() as manager:
        f = int(input("Ingrese el número de filas/columnas de la matriz: "))
        A = leer_matriz(f, manager) 
        B = leer_matriz(f, manager)
        C = manager.list([manager.list([manager.list([0]*f) for _ in range(f)]) for _ in range(f)])

        P = [(i,j,k) for i in range(0,f) for j in range(0,f) for k in range(0,f)]
        processes = []
        for pos in P:
            p = mp.Process(target=llenar, args=(A,B,C, *pos))
            processes.append(p)
            p.start()
        for p in processes:
            p.join()

        for s in range(0,int(math.log2(f))):
            P= [(i+1,j+1,k+1,s+1) for i in range(0,f) for j in range(0,f) for k in range(0,int(f/2))]
            processes = []
            for pos in P:
                p = mp.Process(target=sumar, args=(C, *pos))
                processes.append(p)
                p.start()
            for p in processes:
                p.join()

        s = ''
        for m in range(0,f):
            s += '['
            for n in range (0,f):
                s = s + str(C[m][n][f-1])+', '
            s += ']\n'
        print(f'\n La matriz A*B es: \n {s}')



if __name__ == "__main__":
    main()
