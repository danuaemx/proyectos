import math
import time
import concurrent.futures
import threading

global A, s


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
def sum_elements(p1, p2):

    global A

    A[p2 - 1] += A[p1 - 1]
    print(f'Suma de A[{p2}] = A[{p1}] + A[{p2}] en t={time.time() - s}')

def main():

    global A, s

    A = leer()
    n = int(math.log2(len(A)))
    n2 = len(A)
    s = time.time()

    for i in range(1, n + 1):

        print('Paso nuevo ' + str(i))

        k = pow(2, i)
        k0 = int(k / 2)
        m = int(n2 / k)
        P = [(j * k - k0, j * k) for j in range(1, m + 1)]

        with concurrent.futures.ThreadPoolExecutor(max_workers=m) as executor:
            executor.map(lambda pos: sum_elements(*pos), P)

        print(A)
        
    print('Resultado')
    print(f'{A[n2 - 1]} en t={time.time() - s}')

if __name__ == "__main__":
    main()

