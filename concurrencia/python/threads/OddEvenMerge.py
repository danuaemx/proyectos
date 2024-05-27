import time
import numpy as np
import concurrent.futures

def print_arr(aux, p_i, l):
    print("\n [", end="")
    for i in range(l):
        p = i + p_i
        print(f"{aux[p]:.6f}, ", end="")
    print("]")

def odd_even_split(aux, odd, even, i):
    odd[i] = aux[2*i+1]
    even[i] = aux[2*i]
    print(f'split {2*i+1} y {2*i}')

def unir(aux, odd, even, i):
    aux[2*i+1] = odd[i]
    aux[2*i] = even[i]
    print(f'unir {2*i+1} y {2*i}')

def comparar(aux,i):
    print(f'comparar {2*i-1} y {2*i}')
    if aux[2*i-1] > aux[2*i]:
        aux[2*i-1], aux[2*i] = aux[2*i], aux[2*i-1]

def odd_even_merge(aux, l):
    print(f'odd-even-merge {aux}')
    if l == 2:
        if aux[0] > aux[1]:
            aux[0], aux[1] = aux[1], aux[0]
    else:
        m = l // 2
        
        odd = np.zeros(m)
        even = np.zeros(m)

        P=[(aux, odd, even, i) for i in range(m)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=m) as executor:
            executor.map(lambda pos:  odd_even_split(*pos), P)

        P=((odd,m),(even,m))
        with concurrent.futures.ThreadPoolExecutor(max_workers=m) as executor:
             executor.map(lambda pos:  odd_even_merge(*pos), P)
        
        P=[(aux, odd, even, i) for i in range(m)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=m) as executor:
            executor.map(lambda pos:  unir(*pos), P)

        P=[(aux, i) for i in range(1,m)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=m) as executor:
            executor.map(lambda pos:  comparar(*pos), P)

def odd_even_merge_sort(aux, l):
    if l > 1:
        print(f'odd-even-merge-sort {aux}')
        m = l // 2

        P=((aux[:m],m),(aux[m:], m))
        with concurrent.futures.ThreadPoolExecutor(max_workers=l*l*l) as executor:
            executor.map(lambda pos:  odd_even_merge_sort(*pos), P)

        odd_even_merge(aux, l)

def main():
    n1 = int(input("Ingrese la potencia k, para 2^k renglones de 1 a 10: "))
    n2 = 2 ** n1
    print(f"Ordenar vector de {n2}")

    L = np.zeros(n2)
    print("Ingresar V")
    for i in range(n2):
        L[i] = float(input(f"Ingresar V[{i+1}]: "))

    start_time = time.time()
    odd_even_merge_sort(L, n2)
    end_time = time.time()

    print("\nTiempo de ejecución:", end_time - start_time, "segundos")
    print("\nEl vector resultante:")
    print_arr(L, 0, n2)

if __name__ == "__main__":
    main()
