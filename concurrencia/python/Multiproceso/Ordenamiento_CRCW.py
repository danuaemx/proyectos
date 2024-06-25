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

# Función que realiza la suma de dos elementos en un arreglo
def com(A,Aord,p1, p2):

    if A[p1-1]>=A[p2-1]:
        Aord[p1-1] +=1
    else:
        Aord[p2-1] +=1
    print(list(Aord))

def asign(A,A1,Aord,i):
    A1[int(Aord[i-1])]= A[i-1]
    print(list(A1))


if __name__ == "__main__":
    
    Aux = leer()
    n2 = len(Aux)

    A = mp.Array('d', list(Aux))
    Aord = mp.Array('d',[0]*len(Aux))
    A1 = mp.Array('d',[0]*len(Aux))
    
    P = [(i,j) for i in range(1, n2+1) for j in range(i+1,n2+1)]
    processes = []
    for pos in P:
        p = mp.Process(target=com, args=(A,Aord, *pos))
        processes.append(p)
        p.start()

        # Esperar a que todos los procesos terminen
    for p in processes:
        p.join()
        

    P = [i for i in range(1,n2+1)]
    processes = []
    for pos in P:
        p = mp.Process(target=asign, args=(A,A1,Aord,pos))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print(f'El arreglo ordenado {list(A1)}')
