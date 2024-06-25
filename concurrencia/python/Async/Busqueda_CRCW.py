import asyncio

global A, Amin

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
async def com(p1, p2):
    global A, Amin
    if A[p1-1] >= A[p2-1]:
        Amin[p1-1] = 1
    else:
        Amin[p2-1] = 1
    print(Amin)

async def asign(i):
    global A, Amin
    if Amin[i-1] == 0:
        print(f'El menor es {A[i-1]} en la posición {i}')

async def main():
    global A, Amin
    A = leer()
    n2 = len(A)
    Amin = [0] * len(A)
    P = [(i, j) for i in range(1, n2+1) for j in range(i+1, n2+1)]
    await asyncio.gather(*[com(*pos) for pos in P])
    P = [i for i in range(1, n2+1)]
    await asyncio.gather(*[asign(pos) for pos in P])

if __name__ == "__main__":
    asyncio.run(main())