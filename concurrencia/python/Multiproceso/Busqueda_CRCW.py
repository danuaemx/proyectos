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

    if A[p1-1]>A[p2-1]:
        Aord[p1-1] =1
    elif A[p1-1]==A[p2-1]:
        pass
    else:
        Aord[p2-1] =1
    print(list(Aord))

def asign(A,Aord,i):
    if Aord[i-1] == 0:
        print(f'Minimo {list(A)[i-1]} en {i}')

    

if __name__ == "__main__":
    Aux = leer()
    n2 = len(Aux)

    A = mp.Array('d', list(Aux))
    Aord = mp.Array('d',[0]*len(Aux))
    
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
        p = mp.Process(target=asign, args=(A,Aord,pos))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()