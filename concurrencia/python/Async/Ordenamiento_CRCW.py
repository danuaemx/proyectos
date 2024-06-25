import asyncio

global A,Aord, A1

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

    global A,Aord

    if A[p1-1]>=A[p2-1]:
        Aord[p1-1] +=1
    else:
        Aord[p2-1] +=1
    print(Aord)

async def asign(i):
    global A, A1
    A1[Aord[i-1]]= A[i-1]
    print(A1)


async def main():

    global A,Aord, A1

    A = leer()
    n2 = len(A)
    Aord = [0]*len(A)
    A1 = [0]*len(A)
    P = [(i,j) for i in range(1, n2+1) for j in range(i+1,n2+1)]
    await asyncio.gather(*[com(*pos) for pos in P])

    P = [i for i in range(1,n2+1)]
    await asyncio.gather(*[asign(i) for i in P])
    
    print(f'El arreglo ordenado {A1}')

if __name__ == "__main__":
    asyncio.run(main())
