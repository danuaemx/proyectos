import numpy as np
import asyncio
import time

async def print_arr(aux, p_i, l):
    print("\n [", end="")
    for i in range(l):
        p = i + p_i
        print(f"{aux[p]:.6f}, ", end="")
    print("]")

async def odd_even_split(aux, odd, even, i):
    odd[i] = aux[2*i+1]
    even[i] = aux[2*i]
    print(f'split {2*i+1} y {2*i}')

async def unir(aux, odd, even, i):
    aux[2*i+1] = odd[i]
    aux[2*i] = even[i]
    print(f'unir {2*i+1} y {2*i}')

async def comparar(aux,i):
    print(f'comparar {2*i-1} y {2*i}')
    if aux[2*i-1] > aux[2*i]:
        aux[2*i-1], aux[2*i] = aux[2*i], aux[2*i-1]

async def odd_even_merge(aux, l):
    print(f'odd-even-merge {aux}')
    if l == 2:
        if aux[0] > aux[1]:
            aux[0], aux[1] = aux[1], aux[0]
    else:
        m = l // 2
        
        odd = np.zeros(m)
        even = np.zeros(m)
        tasks = []
        for i in range(m):
            tasks.append(odd_even_split(aux, odd, even, i))
        await asyncio.gather(*tasks)
        
        tasks = []
        tasks.append(odd_even_merge(odd, m))
        tasks.append(odd_even_merge(even, m))
        await asyncio.gather(*tasks)
        
        tasks = []
        for i in range(m):
            tasks.append(unir(aux, odd, even, i))
        await asyncio.gather(*tasks)
        
        tasks = []
        for i in range(1, m):
            tasks.append(comparar(aux, i))
        await asyncio.gather(*tasks)

async def odd_even_merge_sort(aux, l):
    if l > 1:
        print(f'odd-even-merge-sort {aux}')
        m = l // 2
        tasks = []
        tasks.append(odd_even_merge_sort(aux[:m], m))
        tasks.append(odd_even_merge_sort(aux[m:], m))
        await asyncio.gather(*tasks)
        await odd_even_merge(aux, l)

async def main():
    n1 = int(input("Ingrese la potencia k, para 2^k renglones de 1 a 10: "))
    n2 = 2 ** n1
    print(f"Ordenar vector de {n2}")
    L = np.zeros(n2)
    print("Ingresar V")
    for i in range(n2):
        L[i] = float(input(f"Ingresar V[{i+1}]: "))
    start_time = time.time()
    await odd_even_merge_sort(L, n2)
    end_time = time.time()
    print("\nTiempo de ejecución:", end_time - start_time, "segundos")
    print("\nEl vector resultante:")
    await print_arr(L, 0, n2)

if __name__ == "__main__":
    asyncio.run(main())