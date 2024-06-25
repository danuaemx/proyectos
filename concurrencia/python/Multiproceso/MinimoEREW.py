import math
import time
import multiprocessing as mp

global A,s

def leer():
     # Pedir al usuario el tamaño del arreglo
    n = int(input("Ingrese el tamaño del arreglo: "))
    # Crear un arreglo vacío
    arreglo = []
    # Pedir al usuario que ingrese los elementos del arreglo uno por uno
    print("Ingrese los elementos del arreglo, uno por uno:")
    for i in range(n):
        elemento = float(input(f"Elemento {i + 1}: "))
        arreglo.append(elemento)
    return arreglo
    
def ordenar(A,p1,p2):

    if A[p2] >= A[p1]:
        A[p2]= 1000000000
    else:
        A[p1]=A[p2]
        A[p2]=1000000000
    print(list(A))
        
def main():

    global A,s
    A = leer()
    n = int(math.log2(len(A)))
    n2 = len(A)
    s = time.time()
    print(A)
    A = mp.Array('d', list(A))
    for i in range(1, n + 1):
        print('Paso nuevo ' + str(i))
        k = pow(2, i)
        k0 = int(k / 2)
        m = int(n2 / k)
        P = [(n2-j * k,n2+k0-j * k) for j in range(1, m + 1)]
        print(P)
        processes = []
        for pos in P:
            p = mp.Process(target=ordenar,args=(A,*pos))
            processes.append(p)
            p.start()
    for p in processes:
        p.join()
    print(f'Mínimo es {list(A)[0]}')
        
if __name__ == "__main__":
    main()
