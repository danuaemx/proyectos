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

def llenar(Aux,p1,p2):
    Aux[p2-1]=Aux[p1-1]
    print(list(Aux))

# Función que realiza la suma de dos elementos en un arreglo
def cmp(A,Aux,ps,p1):
    if(Aux[p1-1]!=A[p1-1]):
        A[p1-1] = 1000000000
    else:
        ps[0] = 1
        ps[1] = p1
    print(list(A))
    
        
def main():
    A0 = leer()
    n = int(math.log2(len(A0)))
    n2 = len(A0)
    s = time.time()
    Aux = [0]*n2
    Aux[0]=float(input(f"Ingrea el elemento a buscar: "))
    print(Aux)

    Aux = mp.Array('d', list(Aux))
    A = mp.Array('d', list(A0))
    ps = mp.Array('d', [0,0])

    for i in range(1, n + 1):

        print('Paso ' + str(i))

        k = pow(2, i)
        k0 = int(k / 2)
        P = [(j, j+k0) for j in range(1, k0+1)]
        processes = []
        for pos in P:
            p = mp.Process(target=llenar,args=(Aux,*pos))
            processes.append(p)
            p.start()
        for p in processes:
            p.join()
    P = [j for j in range(1, n2+1)]
    print(P)
    processes = []
    for pos in P:
        p = mp.Process(target=cmp, args=(A,Aux,ps,pos))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    if list(ps)[0]==0:
        print('Elemento no encontrado')
    else:
        print('Elemento encontrado en la posición: ',list(ps)[1])
        
if __name__ == "__main__":
    main()
