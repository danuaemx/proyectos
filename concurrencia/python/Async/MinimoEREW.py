import asyncio
import math
import time

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

async def ordenar(p1, p2):
    global A
    if A[p1] == 'Infinito' and A[p2] == 'Infinito':
        pass
    elif A[p1] != 'Infinito':
        pass
    else:
        A[p1] = A[p2]
    if A[p1] != 'Infinito' and A[p2] != 'Infinito' and A[p2] >= A[p1]:
        A[p2] = 'Infinito'
    else:
        A[p1] = A[p2]
        A[p2] = 'Infinito'
    print(A)


async def main():
    global A, s
    p = 'No'
    A = leer()
    n = int(math.log2(len(A)))
    n2 = len(A)
    s = time.time()
    print(A)
    for i in range(1, n + 1):
        print('Paso nuevo ' + str(i))
        k = pow(2, i)
        k0 = int(k / 2)
        m = int(n2 / k)
        P = [(n2 - j * k, n2 + k0 - j * k) for j in range(1, m + 1)]
        print(P)
        await asyncio.gather(*[ordenar(*pos) for pos in P])
    print(f'Mínimo es {A[0]}')


if __name__ == "__main__":
    asyncio.run(main())