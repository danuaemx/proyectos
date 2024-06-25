import math
import time
import multiprocessing as mp

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

# Función que realiza la suma de dos elementos en un arreglo
def sum_elements(A,An,p1, p2):

    A[p2 - 1] =An[p2-1] + An[p1 - 1]
    print(f'Suma de A[{p2}] = A[{p1}] + A[{p2}] en t={time.time()}')


if __name__ == "__main__":
    
    Aux =leer()
    n = int(math.log2(len(Aux)))
    n2 = len(Aux)
    s = time.time()
    An = mp.Array('d', list(Aux))
    A =  mp.Array('d', list(Aux))


    for i in range(1, n + 1):
        print('Paso ' + str(i))
        An =  mp.Array('d', list(A))
        k = pow(2, i)
        k0 = int(k / 2)
        P = [(j-k0, j) for j in range(k0+1, n2+1)]

        processes = []
        for pos in P:
            p = mp.Process(target=sum_elements, args=(A,An, *pos))
            processes.append(p)
            p.start()

        # Esperar a que todos los procesos terminen
        for p in processes:
            p.join()
        
    print('Resultado')
    print(f'{A[n2 - 1]} en t={time.time() - s}')
