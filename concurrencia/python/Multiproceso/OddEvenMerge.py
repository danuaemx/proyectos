import multiprocessing as mp
import numpy as np
import time

#Método para mp.arrays compartidos entre subprocesos

def asignar_datos(data, odd, even, i):
    if i%2==0:
        even[i//2] = data[i]
    else:
        odd[i//2] = data[i]

def unir_datos(data, odd, even, i):
    data[2*i+1] = odd[i]
    data[2*i] = even[i]

def comparar_datos(data,i):
    if data[2*i-1] > data[2*i]:
        data[2*i-1], data[2*i] = data[2*i], data[2*i-1]

#Clases de herencia de mp.Process para subprocesos de OddEvenMergeSort
    """Cada uno de estos métodos hereda de mp.Process y sobreescribe
    implementa for paralelo usando mp.Process para dividir, unir y comparar,
    con un arreglo compartido entre los procesos hijos y el proceso padre (mp.array).
    Finamente se transmiten los datos procesados al proceso padre."""

class OddEvenSplit(mp.Process):
    
    #Constructor modificado
    def __init__(self, data, queue):
        #Proceso herencia
        mp.Process.__init__(self)
        #Atributos data, odd, even, n, queue_padre, shared_odd, shared_even
        self.queue_padre = queue
        self.data = data
        #Obtener tamaño de data
        self.n = len(data)
        #Crear arreglos odd y even vacios
        self.odd = np.zeros(self.n//2)
        self.even = np.zeros(self.n//2)
        #Crear arreglos compartidos
        self.shared_data = mp.Array('d', self.data)
        self.shared_odd = mp.Array('d', self.odd)
        self.shared_even = mp.Array('d', self.even)
        
    def split(self):
        processes = []
        for i in range(self.n):
            p = mp.Process(target=asignar_datos,
                           args=(self.shared_data, 
                                 self.shared_odd, 
                                 self.shared_even, i))
            processes.append(p)
            p.start()
        for p in processes:
            p.join()
        self.odd = np.array(list(self.shared_odd))
        self.even = np.array(list(self.shared_even))
    
        #Metodo run modificado
    def run(self):
        print(f'Split en {mp.current_process().name} \n')
        self.split()
        self.queue_padre.put((self.even, self.odd))


    
    #Constructor modificado
    def __init__(self, data, queue):
        #Proceso herencia
        mp.Process.__init__(self)
        #Atributos data, odd, even, n, queue_padre, shared_odd, shared_even
        self.queue_padre = queue
        self.data = data
        #Obtener tamaño de data
        self.n = len(data)
        #Crear arreglos odd y even vacios
        self.odd = np.zeros(self.n//2)
        self.even = np.zeros(self.n//2)
        #Crear arreglos compartidos
        self.shared_data = mp.Array('d', self.data)
        self.shared_odd = mp.Array('d', self.odd)
        self.shared_even = mp.Array('d', self.even)
        
    def split(self):
        processes = []
        for i in range(self.n):
            p = mp.Process(target=asignar_datos,
                           args=(self.shared_data, 
                                 self.shared_odd, 
                                 self.shared_even, i))
            processes.append(p)
            p.start()
        for p in processes:
            p.join()
        self.odd = np.array(list(self.shared_odd))
        self.even = np.array(list(self.shared_even))
    
        #Metodo run modificado
    def run(self):
        print(f'Split en {mp.current_process().name} \n')
        self.split()
        self.queue_padre.put((self.even, self.odd))

class Unir(mp.Process):

    #Constructor modificado
    def __init__(self, data, odd, even, queue):
        #Proceso herencia
        mp.Process.__init__(self)
        #Atributos data, odd, even, n, queue_padre, shared_odd, shared_even
        self.queue_padre = queue
        self.data = data
        #Obtener tamaño de data
        self.n = len(data)
        self.odd = odd
        self.even = even
        #Crear arreglos compartidos
        self.shared_data = mp.Array('d', self.data)
        self.shared_odd = mp.Array('d', self.odd)
        self.shared_even = mp.Array('d', self.even)

    #Metodo run modificado
    def run(self):
        print(f'Unir en {mp.current_process().name} \n')
        self.unir()
        #Transmitir datos a padre
        self.queue_padre.put(self.data)

    def unir(self):
        processes = []
        for i in range(self.n//2):
            p = mp.Process(target=unir_datos, 
                           args=(self.shared_data, 
                                 self.shared_odd, 
                                 self.shared_even,i))
            processes.append(p)
            p.start()
        for p in processes:
            p.join()
        self.data = np.array(list(self.shared_data))

class Comparar(mp.Process):

    #Constructor modificado
    def __init__(self, data, queue):
        #Proceso herencia
        mp.Process.__init__(self)
        #Atributos data, n, queue_padre, queue_hijos
        self.data = data
        self.n = len(data)
        self.queue_padre = queue
        self.shared_data = mp.Array('d', self.data)

    #Metodo run modificado
    def run(self):
        print(f'Comparar en {mp.current_process().name} \n')
        self.comparar()
        #Transmitir datos a padre
        self.queue_padre.put(self.data)

    def comparar(self):
        processes = []
        for i in range(1,self.n//2):
            p = mp.Process(target=comparar_datos, 
                           args=(self.shared_data, i))
            processes.append(p)
            p.start()
        for p in processes:
            p.join()
        self.data = np.array(list(self.shared_data))

#Llamadas recursivas implementadas como llamadas al constructor en la misma clase
"""Para la clase OddEvenMerge se implementa la llamada recursiva paralela
    como la creación de un nuevo proceso con herencia de mp.Process
    divide el arreglo en dos partes (odd y even) usando un proceso
    Split, luego crea dos procesos hijos con su constructor para ordenar cada parte,
    une las partes ordenadas con un proceso Unir y compara los elementos con un proceso
    Comparar. Finalmente transmite los datos ordenados al padre."""

class OddEvenMerge(mp.Process):

    #Constructor modificdo
    def __init__(self, data,queue):
        #Proceso herencia
        mp.Process.__init__(self)
        #Atributos data, n, queue_padre, queue_hijos
        self.data = data
        self.n = len(data)
        self.queue_padre = queue
        self.queue_hijos = [mp.Queue() for i in range(2)]
        self.queue_split = mp.Queue()
        self.queue_unir = mp.Queue()
        self.queue_comparar = mp.Queue()

    #Metodo run modificado
    def run(self):
        self.oddEvenMerge()
        #Transmitir datos a padre
        self.queue_padre.put(self.data)

    def oddEvenMerge(self):
        if self.n==2:
            print(f'Caso base OddEvenMerge en {mp.current_process().name} \n')
            if self.data[0]>self.data[1]:
                self.t = self.data[0]
                self.data[0] = self.data[1]
                self.data[1] = self.t
        elif self.n > 1:
            #Obtener odd y even
            p1 = OddEvenSplit(self.data, self.queue_split)
            p1.start()
            p1.join()
            #Recibir odd y even
            self.even, self.odd = self.queue_split.get()
            
            #Crear procesos hijos odd e even
            p2 = OddEvenMerge(self.even, 
                              self.queue_hijos[0])
            p2.start()
            p3 = OddEvenMerge(self.odd, 
                              self.queue_hijos[1])
            p3.start()
            p2.join()
            p3.join()

            #Obtener odd y even del queue_hijos
            self.even = self.queue_hijos[0].get()
            self.odd = self.queue_hijos[1].get()

            #Unir odd y even
            p4 = Unir(self.data, self.odd, self.even, 
                      self.queue_unir)
            p4.start()
            p4.join()
            #Recibir data
            self.data = self.queue_unir.get()
            
            #Comparar odd y even
            p5 = Comparar(self.data, 
                          self.queue_comparar)
            p5.start()
            p5.join()
            #Recibir data
            self.data = self.queue_comparar.get()  

"""Para la clase OddEvenMergeSort se implementa la llamada recursiva paralela
    como la creación de un nuevo proceso con herencia de mp.Process
    con el constructor de la clase divide el arreglo en dos partes 
    y crea dos procesos hijos para ordenar cada parte, luego crea un 
    proceso hijo OddEvenMerge para ordenar el arreglo completo.
    Finalmente transmite los datos ordenados al padre."""

class OddEvenMergeSort(mp.Process):

    #Constructor modificdo
    def __init__(self, data, queue):
        #Proceso herencia
        mp.Process.__init__(self)
        #Atributos data, n, queue_padre, queue_hijos
        self.data = data
        self.queue_padre = queue
        self.n = len(data)
        self.queues_hijos = [mp.Queue() for i in range(3)]
    
    #Metodo run modificado
    def run(self):
        self.oddEvenMergeSort()
        #Transmitir datos a padre
        self.queue_padre.put(self.data)

    def oddEvenMergeSort(self):
        if self.n>1:
            m = self.n // 2

            #Crear procesos hijos
            p1 =OddEvenMergeSort(self.data[:m], 
                                 self.queues_hijos[0])
            p2 =OddEvenMergeSort(self.data[m:], 
                                 self.queues_hijos[1])
            print(f'Llamada recursiva oddEvenMergeSort en {mp.current_process().name} \n')
            p1.start()
            p2.start()
            p1.join()
            p2.join()
            #Recibir datos de los hijos
            self.data[:m],self.data[m:] = self.queues_hijos[0].get() , self.queues_hijos[1].get()
            #Crear proceso hijo OddEvenMerge
            p3 = OddEvenMerge(self.data, 
                              self.queues_hijos[2])
            print(f'Llamada oddEvenMerge en oddEvenMergeSort en {mp.current_process().name} \n')
            p3.start()
            p3.join()
            #Recibir datos de OddEvenMerge
            self.data = self.queues_hijos[2].get()

#Método principal

def iniciar():
    print('Odd-Even Merge Sort')
    print('-------------------')
    print('Ordena un arreglo aleatorio de 16 elementos -100<e<100')
    data = np.random.randint(-100, 100, 16)
    print('Data inicial:', data)
    input("Presiona Enter para continuar(Click en la linea previo)...")
    queue = mp.Queue()
    inicio = time.time()
    p = OddEvenMergeSort(data, queue)
    p.start()
    p.join()
    fin = time.time()
    print(f'Ejecución en {fin-inicio} segundos \n')
    print(f'Data final: {queue.get()}')

if __name__ == '__main__':
    iniciar()