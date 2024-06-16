#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 20:36:04 2024

@author: daniel
"""

class Control:
    
    def __init__(self,modelo,vista):
        self.__modelo = modelo
        self.__vista = vista
        
    def iniciar(self):
        print('control set')
        self.__modelo.set_control(self)
        self.__vista.set_control(self)
        
    def abrir(self,ruta):
       pagina = self.__modelo.abrir(ruta)
       self.__vista.pagina(1, pagina)
    
    def botones(self,clave):
        pagina = self.__modelo.paginas(clave)
        if pagina == 'lim':
            pass
        else:
            self.__vista.pagina(clave, pagina)
            
    def interpretar(self):
        pagina = self.__modelo.interpretar()
        self.__vista.pagina(3, pagina[0])
        self.__vista.pagina(5,pagina[1])
        self.__vista.pagina(7,pagina[2])
       

