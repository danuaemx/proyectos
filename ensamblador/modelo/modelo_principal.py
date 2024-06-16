#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 20:36:34 2024

@author: daniel
"""
from .fase1 import Fase1
from .fase2 import Fase2
class Modelo:
    def __init__(self):
        #Inicia índice de tablas en -1 ya que son incorrectos por default
        self.__indice_f2_tabla_var = -1
        self.__indice_f2_tabla_code = -1
        self.__indice_f1 = -1
        self.__indice = -1
    
    def set_control(self,control):
        #Establece el control de la clase
        self.__control = control
        print('modelo-control')
         
    def abrir(self,ruta):
        
        #Abrir contenido
        with open(ruta,'r') as ens:
            self.__contenido = ens.read()
            
        #Contenido preparado (sin comentarios y tabs)
        self.__lineas = self.__contenido.split('\n')
        lineas1 = []
        for linea in self.__lineas:
            i = linea.find(';')
            if i > -1:
               lineas1.append(linea[:i])
            else:
                lineas1.append(linea)
        lineas1 = [linea.strip() for linea in lineas1 if linea.strip()]
        
        #Texto 000.txt y paginación
        self.__paginas = []
        self.__indice = 0
        
        paginatxt = ''
        lineastxt = ''
        n = 0
        
        
        for linea in lineas1:
            
            n += 1
            lineastxt += f'{n}\t{linea}\n'
            paginatxt   += f'{n}\t{linea}\n'
            
            if n%15 == 0:
                self.__paginas.append(paginatxt)
                paginatxt = ''
        self.__paginas.append(paginatxt)
        
        #Escribir
        with open('.tmp/000.txt', 'w', encoding='utf-8') as fase0:
            fase0.write(f'0\tFase0\n{lineastxt}')
                
       
        return self.__paginas[0]
    
    def interpretar(self):
        #Usa la clase Fase1 para hacer la clasificación
        fase1 = Fase1()
        fase1.clasificar_t()
        
        #paginar, establece el índice en valor correcto
        
        self.__indice_f1 = 0
        self.__paginas_f1 = []
        
        with open('.tmp/001.txt','r') as fase1_txt:
            self.__fase1_cont = fase1_txt.read()
        #Lee el archivo preparado y en forma por la clase Fase1    
        fase1_lineas = self.__fase1_cont.split('\n')
        n1 = 0
        paginatxt1 = ''
        #Comienza la sepración por cada linea y la pagina a 15 renglones
        for linea in fase1_lineas:
            n1 +=1
            paginatxt1 += f'{linea}\n'
            if n1%15 == 0:
                self.__paginas_f1.append(paginatxt1)
                paginatxt1 = ''
        self.__paginas_f1.append(paginatxt1)
        #Inicia la fase2 con la clase Fase2 y llama al método verificar
        self.__fase2 = Fase2()
        self.__fase2.verificar()
        #Obtiene las tablas de la instancia
        self.__tabla_simbolos = self.__fase2.get_tabla()
        self.__tabla_code = self.__fase2.get_lineas()
        #Incializa indices erroneos por default
        self.__indice_f2_tabla_var = 1
        self.__indice_f2_tabla_code = 1
        
        #Regresa la página 0 de fase1 y de las tablas de la fase2
        self.__k = 9
        return self.__paginas_f1[0], self.paginas(5), self.paginas(7)
            
    def paginas(self,clave):
        #Actualiza el índice según la clave y devuelve la página
        match clave:
            #Página anterior de contenido
            case 1:
                
                if (self.__indice - 1)<0:
                    return 'lim'
                else:
                    self.__indice -= 1
                    return self.__paginas[self.__indice]
            #Página siguiente de contenido
            case 2:
                
                if (self.__indice + 1) >= len(self.__paginas):
                    return 'lim'
                else:
                    self.__indice += 1
                    return self.__paginas[self.__indice]
            #Página anterior de fase 1
            case 3:
                
                if (self.__indice_f1 - 1)<0:
                    return 'lim'
                else:
                    self.__indice_f1 -= 1
                    return self.__paginas_f1[self.__indice_f1]
            #Página siguiente de fase  1
            case 4:
                
                if (self.__indice_f1 + 1) >= len(self.__paginas_f1):
                    return 'lim'
                else:
                    self.__indice_f1 += 1
                    return self.__paginas_f1[self.__indice_f1]
            #Página anterior de tabla de símbolos
            case 5:
                if (self.__indice_f2_tabla_var-1)<0:
                    return 'lim'
                else:
                    self.__indice_f2_tabla_var -= 1
                    return self.__tabla_simbolos[self.__k*self.__indice_f2_tabla_var:self.__k*(self.__indice_f2_tabla_var+1)]
            #Página siguiente de tabla de símbolos
            case 6:
                if self.__k*(self.__indice_f2_tabla_var+1)>len(self.__tabla_simbolos):
                    return 'lim'
                else:
                    self.__indice_f2_tabla_var += 1
                    try:
                        return self.__tabla_simbolos[self.__k*self.__indice_f2_tabla_var:self.__k*(self.__indice_f2_tabla_var+1)]
                    except:
                        return self.__tabla_simbolos[self.__k*self.__indice_f2_tabla_var:]
            #Página anterior de lineas de código
            case 7:
                if (self.__indice_f2_tabla_code-1)<0:
                    return 'lim'
                else:
                    self.__indice_f2_tabla_code -= 1
                    return self.__tabla_code[self.__k*self.__indice_f2_tabla_code:self.__k*(self.__indice_f2_tabla_code+1)]
            #Página siguiente de lineas de código
            case 8:
                if self.__k*(self.__indice_f2_tabla_code+1)>len(self.__tabla_code):
                    return 'lim'
                else:
                    
                    self.__indice_f2_tabla_code += 1
                    try:
                        return self.__tabla_code[self.__k*self.__indice_f2_tabla_code:self.__k*(self.__indice_f2_tabla_code+1)]
                    except:
                        return self.__tabla_code[self.__k*self.__indice_f2_tabla_code:]
                
            
                
        
        
        