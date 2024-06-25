import math
import time
import asyncio

global A,An, s

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
async def sum_elements(p1, p2):

    global A,An

    A[p2 - 1] =An[p2-1] + An[p1 - 1]
    print(f'Suma de A[{p2}] = A[{p1}] + A[{p2}] en t={time.time() - s}')

async def main():

    global A,An, s

    A =leer()
    n = int(math.log2(len(A)))
    n2 = len(A)
    s = time.time()

    for i in range(1, n + 1):

        An = list(A)

        print('Paso ' + str(i))

        k = pow(2, i)
        k0 = int(k / 2)
        P = [(j-k0, j) for j in range(k0+1, n2+1)]

        await asyncio.gather(*[sum_elements(*pos) for pos in P])

        print(A)
        
    print('Resultado')
    print(f'{A[n2 - 1]} en t={time.time() - s}')

if __name__ == "__main__":
    asyncio.run(main())