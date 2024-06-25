import asyncio
import math
import time

global A, Aux, s, p


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


async def llenar(p1, p2):
    global Aux
    Aux[p2 - 1] = Aux[p1 - 1]


# Función que realiza la suma de dos elementos en un arreglo
async def cmp(p1):
    global A, Aux, p
    if (Aux[p1 - 1] != A[p1 - 1]):
        A[p1 - 1] = 'Infinito'
    else:
        p = p1
    print(A)

async def main():
    global A, Aux, s, p
    p = 'No'
    A = leer()
    n = int(math.log2(len(A)))
    n2 = len(A)
    s = time.time()
    Aux = [0] * n2
    Aux[0] = float(input(f"Ingrea el elemento a buscar: "))
    print(Aux)
    for i in range(1, n + 1):
        print('Paso ' + str(i))
        k = pow(2, i)
        k0 = int(k / 2)
        P = [(j, j + k0) for j in range(1, k0 + 1)]
        await asyncio.gather(*[llenar(*pos) for pos in P])
        print(Aux)
    P = [j for j in range(1, n2 + 1)]
    print(P)
    await asyncio.gather(*[cmp(pos) for pos in P])
    print(A)
    if p == 'No encontrado':
        print(p)
    else:
        print(f'encontrado en {p}')


if __name__ == "__main__":
    asyncio.run(main())