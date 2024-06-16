#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 17:18:25 2024

@author: daniel
"""
from .variables import *
from .fase3 import Decodificador

class Fase2:
    def __init__(self):
        with open('.tmp/001.txt','r') as fase1:
            self.__contenido = fase1.read()
        #print(self.__contenido)
        #Incluye etiquetas  e indices de fácil acceso  
        self.__tabla_vars = []
        self.__indice_vars = []
        self.__indice_etq = []
        #Lista de lineas correctas o no
        self.__lineas_verificadas = []
        #Linesas iniciales que se procesan
        self.__lineas = []
        #-1 si no se ha encontrado por default
        self.__stack_ind = -1
        self.__data_ind = -1
        self.__code_ind = -1
        #Decodificador para tablas e instrucciones
        self.__decodificador = Decodificador(self)
        
        #Origen hipotético de la memoria 128 o 0x0080
        self.__org = 592

        #Contador
        self.__cont_seg_inst = self.__org
        
    def verificar_stack(self):
        #Variable para verificar si el segmento termina con ends
        self.__end = False
        #Variable para verificar si hay más de una declaración válida
        self.__primero = False
        # De inicio a stack
                                        #En el origen
        self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                          #La pseudinstrucción
                                          self.__lineas[self.__stack_ind][0][0],
                                          #No aplicable
                                          'N/A',
                                          #Correcto por default
                                          'correcto'))
        # De stack a data se recorre la lista de lineas
        for i in range (self.__stack_ind+1,self.__data_ind):
            #Obtener la línea como cadena
            l = ''
            for t in self.__lineas[i]:
                l += f'{t[0]} '
            #Si ya se encontró un ends
            if self.__end:
                self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                  l,
                                                  'N/A',
                                                  'fuera de segmento'))
            #Si la línea es un ends y no tiene argumentos
            elif self.__lineas[i][0][0] == 'ends' and len(self.__lineas[i]) == 1:
                self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                  l,
                                                  'N/A',
                                                  'correcto'))
                self.__end = True
            #Si la línea tiene 3 argumentos (tipo, inmediato, dup)
            elif len(self.__lineas[i]) == 3:
                #Condiciones para verificar si la línea es correcta

                #----------------------------------------------
                #Tipo dw
                cond1 = 'dw' in self.__lineas[i][0][1]
                #Longitud sin signo
                cond2 = 'numérica' in self.__lineas[i][1][1] and 'signo' not in self.__lineas[i][1][1]
                #Es dupla
                cond3 = 'dupla' in self.__lineas[i][2][1]
                #Si se cumple todo, la línea es correcta
                cond4 = cond1 and cond2 and cond3 and not self.__primero
                #----------------------------------------------

                if cond4:
                    self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                      l,
                                                      'N/A',
                                                      'correcto'))
                    #Actualiza el contador
                    
                    l = self.__decodificador.calcular_tam_sim('dw',self.__lineas[i][1][1],
                                                              self.__lineas[i][2][1],
                                                              self.__lineas[i][1][0])
                    self.__cont_seg_inst += l
                elif self.__primero:
                    self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                      l,
                                                      'N/A',
                                                      'Error: solo una declaración'))
                elif not cond1:
                    self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                      l,
                                                      'N/A',
                                                      'Error: dw'))
                elif not cond2:
                    self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                      l,
                                                      'N/A',
                                                      'Error: tamaño es positivo'))
                elif not cond3:
                    self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                      l,
                                                      'N/A',
                                                      'Error: dup'))
            #Cualquier otro caso   
            else:
                self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                  l,
                                                  'N/A',
                                                  'Error: estructura dw-num-dup'))

    def verificar_data(self):
        #Variable para verificar si el segmento termina con ends
        self.__end = False
        # Inicio de data con pseudoinstrucción
        self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                          self.__lineas[self.__data_ind][0][0],
                                          'N/A',
                                          'correcto'))
        self.__cont_seg_inst = self.__org
        # De data a code va el rango de líneas
        for i in range (self.__data_ind+1,self.__code_ind):
            #Obtener la línea como cadena
            l = ''
            for t in self.__lineas[i]:
                l += f'{t[0]} '
            #Si ya se encontró un ends
            if self.__end:
                self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                  self.__lineas[i][0][0],
                                                  'N/A',
                                                  'fuera de segmento'))
            #Si la línea es un ends y no tiene argumentos
            elif self.__lineas[i][0][0] == 'ends' and len(self.__lineas[i]) == 1:
                self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                  self.__lineas[i][0][0],
                                                  'N/A',
                                                  'correcto'))
                self.__end = True
            #Si la línea tiene 3 argumentos (simbolo, tipo ,inmediato)
            elif len(self.__lineas[i])==3:
                #Condiciones para verificar si la línea es correcta

                #----------------------------------------------
                #Si el argumento es inmediato
                cond0 = 'inmediato' in self.__lineas[i][2][1]
                #Si 'db/dw' esta en el tipo de el inmediato
                cond1 = self.__lineas[i][1][0] in self.__lineas[i][2][1]
                #Si es una constante equ y no es cadena
                cond2 = self.__lineas[i][1][0] == 'equ' and 'letra' not in self.__lineas[i][2][1]
                #Si es un simbolo
                cond3 = 'simbolo' in self.__lineas[i][0][1]
                #Si es un una palabra puede ser db y dw
                cond4 = 'cadena' in self.__lineas[i][2][1] and (self.__lineas[i][1][0] =='dw' or self.__lineas[i][1][0] == 'db' )
                #Si es es cond1 o cond2 o cond4
                cond5 = cond1 or cond2 or cond4
                #No esta en indice_vars
                cond6 = self.__lineas[i][0][0] not in self.__indice_vars
                #Si es con3 y cond5
                cond7 = cond6 and cond3 and cond5 and cond0
                #----------------------------------------------
                
                if cond7:
                    self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                      l,
                                                      'N/A',
                                                      'correcto'))
                    #Identificar el tamaño de la variable     Tipo de tamaño
                    #Si es dupla no hace nada de eso
                    if self.__lineas[i][1][0] == 'equ':
                        l=0
                    else:
                        l = self.__decodificador.calcular_tam_sim(self.__lineas[i][1][0],
                                                              #Sólo en dupla
                                                              '',
                                                              #Tipo de dato descrito
                                                              self.__lineas[i][2][1],
                                                              #Valor específico (Sólo si es cadena)
                                                              self.__lineas[i][2][0])
                    #Agregar a la tabla de variables
                                            #Dirección
                    self.__tabla_vars.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                              #Simbolo
                                              self.__lineas[i][0][0],
                                            #Tipo de tamaño
                                            self.__lineas[i][1][0],
                                            #Tipo de dato
                                            self.__lineas[i][2][1],
                                            #Valor especifico
                                            self.__lineas[i][2][0],
                                            #Tamaño
                                            f'{str(l)}B'))
                    self.__indice_vars.append(self.__lineas[i][0][0])
                    #Actualizar dirección de memoria
                    self.__cont_seg_inst += l

        
                elif not cond3:
                    self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                      l,
                                                      'N/A',
                                                      'Error: simbolo'))
                elif not cond6:
                    self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                      l,
                                                      'N/A',
                                                      'Error: declaracion duplicada'))
                elif not cond1:
                    self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                      l,
                                                      'N/A',
                                                      'Error: solo db/dw como datos'))
                elif not cond2:
                    self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                      l,
                                                      'N/A',
                                                      'Error: equ'))
                
            #Si la línea tiene 4 argumentos (simbolo, tipo, inmediato, dup)
            elif len(self.__lineas[i])==4:
                #Condiciones para verificar si la línea es correcta

                #----------------------------------------------
                #Si el argumento es inmediato [3][1]
                cond0 = 'inmediato' in self.__lineas[i][3][1]
                #Si la longitud es correcta [2][1]
                cond1 = 'constante numérica' in self.__lineas[i][2][1] and 'signo' not in self.__lineas[i][2][1]
                #Si 'db/dw' esta en el tipo de el inmediato
                cond2 = self.__lineas[i][1][0] in self.__lineas[i][3][1]
                #Si es un simbolo
                cond3 = 'simbolo' in self.__lineas[i][0][1]
                #dupla en argumento
                cond4 = 'dupla' in self.__lineas[i][3][1]
                #Si no es cadena    
                cond5 = 'cadena' not in self.__lineas[i][2][1]
                #No esta en indicie_vars
                cond6 = self.__lineas[i][0][0] not in self.__indice_vars
                #Si es correcto
                cond7 = cond0 and cond1 and cond2 and cond3 and cond4 and cond5 and cond6
                #----------------------------------------------

                if cond7:
                    self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                      l,
                                                      'N/A',
                                                      'correcto'))
                                            #Dirección
                    #Identificar el tamaño de la variable     Tipo de tamaño
                    l = self.__decodificador.calcular_tam_sim(self.__lineas[i][1][0],
                                                              #Tipo de longitud
                                                              self.__lineas[i][2][1],
                                                              #Tipo de dato descrito
                                                              self.__lineas[i][3][1],
                                                              #Valor específico la longitud
                                                              self.__lineas[i][2][0])
                    self.__tabla_vars.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                            #Simbolo
                                              self.__lineas[i][0][0],
                                            #Tipo de tamaño
                                            self.__lineas[i][1][0],
                                            #Tipo de dato
                                            self.__lineas[i][3][1],
                                            #Valor especifico
                                            f'{self.__lineas[i][2][0]} {self.__lineas[i][3][0]}',
                                            #Tamaño
                                            f'{str(l)}B'))
                    
                    self.__indice_vars.append(self.__lineas[i][0][0])
                    #Actualizar dirección de memoria
                    self.__cont_seg_inst += l

                elif not cond1:
                    self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                      l,
                                                      'N/A',
                                                      'Error: constante numérica no signo'))
                elif not cond2:
                    self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                      l,
                                                      'N/A',
                                                      'Error: solo db/dw como datos'))
                elif not cond3:
                    self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                      l,
                                                      'N/A',
                                                      'Error: simbolo'))
                elif not cond4:
                    self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                      l,
                                                      'N/A',
                                                      'Error: dup'))
                elif not cond5:
                    self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                      l,
                                                      'N/A',
                                                      'Error: cadena debe ser db/dw'))
                elif not cond6:
                    self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                      l,
                                                      'N/A',
                                                      'Error: declaracion duplicada'))
                
            #Cualquier otro caso
            else:
                self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                  l,
                                                  'N/A',
                                                  'Error: s-tipo- inm/n-dup'))
        
    def verificar_code(self):    
        #Variable para verificar si el segmento termina con ends
        self.__end = False
        # Inicio de data con pseudoinstrucción
        self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                          self.__lineas[self.__code_ind][0][0],
                                          'N/A',
                                          'correcto'))
        #Iniciar el decodificador, para que pueda hacer su función
        self.__decodificador.iniciar()

        #Al origen
        self.__cont_seg_inst = self.__org

        # De data a code va el rango de líneas
        for i in range (self.__code_ind+1,len(self.__lineas)):
            
            #Obtener la línea como cadena
            l = ''
            for t in self.__lineas[i]:
                l += f'{t[0]} '
            #print(l)
            #Si ya se encontró un ends
            if self.__end:
                self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                  self.__lineas[i][0][0],
                                                  'N/A',
                                                  'fuera de segmento'))
            #Si la línea es un ends y no tiene argumentos
            elif self.__lineas[i][0][0] == 'ends'  and len(self.__lineas[i]) == 1:
                self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                  self.__lineas[i][0][0],
                                                  'N/A',
                                                  'correcto'))
                self.__end = True
            #Si es una etiqueta declarada y no hay más en la linea
            elif 'etiqueta' in self.__lineas[i][0][1] and len(self.__lineas[i])==1 and self.__lineas[i][0][0] not in self.__indice_etq:
                #Se reemplaza/elimina ':'
                self.__lineas_verificadas.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                                  self.__lineas[i][0][0].replace(':',''),
                                                  'N/A',
                                                  'nueva etq'))
                self.__tabla_vars.append((str(format(self.__cont_seg_inst, '04x').upper()),
                                          self.__lineas[i][0][0].replace(':',''),
                                          'etiqueta',
                                          'n/a',
                                          'n/a',
                                          'n/a'))
                #Se actualiza el índice de etiquetas
                self.__indice_etq.append(self.__lineas[i][0][0].replace(':',''))
                #Se añaden a la tabla de símbolo
            #Debe ser por fuerza una instrucción o no vale
            else:
                r = self.__decodificador.decodificar(self.__lineas[i])
                #Si es correcto
                #Más importante de la fase 4
                try:
                    if len(l.split()) == 3:
                        l = f'{l.split()[0]} {l.split()[1]} ,{l.split()[2]}'
                    r[1]= l
                    a = r[0]
                    r[0] = format(self.__cont_seg_inst,'04x').upper()
                    self.__cont_seg_inst= self.__cont_seg_inst + a
                    self.__lineas_verificadas.append(r)
                except:
                    r = (format(self.__cont_seg_inst,'04x').upper(),
                         l,
                         'N/A',
                         'Error: instrucción incorrecta')
                
            
    
    def verificar_segmentos(self):
        #Identifica los índices de los segmentos

        for i in range(len(self.__lineas)):
            if self.__lineas[i][0][0] == ps_seg[0] and len(self.__lineas[i]) == 1:
                self.__stack_ind = i
                break
            
        for i in range(len(self.__lineas)):    
            if self.__lineas[i][0][0] == ps_seg[1] and len(self.__lineas[i]) == 1:
                self.__data_ind = i
                break
        for i in range(len(self.__lineas)):    
            if  self.__lineas[i][0][0] == ps_seg[2] and len(self.__lineas[i]) == 1:
                self.__code_ind = i
                break

        #Si se encontraron los segmentos y están en orden
        cond1 = self.__stack_ind < self.__data_ind
        cond2 =  self.__data_ind < self.__code_ind
        cond3 = cond1 and cond2
        
        if cond3:
            return True
        else:
            return False
    #???            
    def calcular_tamaño(self):
        pass
    
    def verificar(self):
        aux = self.__contenido.split('\n')
        #Procesar contenido
        lineas_aux0 = []
        for cad in aux[1:]:
            try:
                cad1 = cad.split('.',1)
                cad2 = f'{cad1[1]}'.split('\t',1)
                cad3 = f'{cad2[1]}'.split('#',1)
                lineas_aux0.append([int(cad1[0]),int(cad2[0]),cad3[0].strip(),cad3[1]])
            except:
                pass
        #print(lineas_aux0)    
        lineas_aux = []
        lineas_aux1 = []
        ind = 1
        
        #Crear matriz [linea][args]
        for linea in lineas_aux0:
            if linea[0] == ind:
                lineas_aux1.append((linea[2],linea[3]))
            else:
                ind +=1
                lineas_aux.append(lineas_aux1)
                lineas_aux1 = []
                lineas_aux1.append((linea[2],linea[3]))
        #Parte tricky para el último elemento ya que es matriz
        #Añadir el último elemento antes añadido a una lista        
        lineas_aux1 = []
        lineas_aux1.append((lineas_aux0[-1][2],lineas_aux0[-1][3]))
        lineas_aux.append(lineas_aux1)
            
         
        self.__lineas = lineas_aux
        #print(len(self.__lineas))
        
        if self.verificar_segmentos():
            #Verificar segmentos
            self.verificar_stack()
            if not self.__end:
                self.__lineas_verificadas.append(('###',
                                                  'No se encontró ends',
                                                  'n',
                                                  'n'))
            self.verificar_data()
            if not self.__end:
                self.__lineas_verificadas.append(('###',
                                                  'No se encontró ends',
                                                  'n',
                                                  'n'))
            #Direcciones de memoria
            self.calcular_tamaño()
            self.verificar_code()
            if not self.__end:
                self.__lineas_verificadas.append(('###',
                                                  'No se encontró ends',
                                                  'n',
                                                  'n'))
        else:
            self.__lineas_verificadas.append(('n',
                                              'n',
                                              '###stack.data.code',
                                              'Error',
                                              'segmentos incorrectos',
                                              'n'))

    def get_tabla(self):
        #Regresa la tabla de simbolos
        return self.__tabla_vars
    def get_lineas(self):
        #Regresa la verificación de lineas
        return self.__lineas_verificadas
    def get_indice(self):
        #Auxiliar para decodificador para etiquetas
        return self.__indice_etq   
    def get_vars(self):
        #Auxiliar para decodificador para variables
        return self.__indice_vars
    def get_etqs(self):
        #Auxiliar para decodificador para etiquetas
        return self.__indice_etq
    
    def get_cont(self):
        return self.__cont_seg_inst
