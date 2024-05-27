import math
import time
import concurrent.futures

global A,Amin

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
def com(p1, p2):

    global A,Amin,Aord

    if A[p1-1]>=A[p2-1]:
        Amin[p1-1] =1
    else:
        Amin[p2-1] =1
    print(Amin)

def asign(i):
    global A, Amin
    if Amin[i-1]==0:
        print(f'El menor es {A[i-1]} en la posición {i}')


def main():

    global A, Amin
    A = leer()
    n2 = len(A)
    Amin = [0]*len(A)
    P = [(i,j) for i in range(1, n2+1) for j in range(i+1,n2+1)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=n2*n2) as executor:
        executor.map(lambda pos: com(*pos), P)

    P = [i for i in range(1,n2+1)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=n2) as executor:
        executor.map(lambda pos: asign(pos), P)

if __name__ == "__main__":
    main()
