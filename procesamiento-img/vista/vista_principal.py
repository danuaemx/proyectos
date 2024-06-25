#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 20:37:00 2024

@author: daniel
"""
from PyQt5.QtWidgets import QApplication
from .gui import Qt_ventana
import sys

class Vista():
    def __init__(self):
        
        #Permitir que la aplicación maneje argumentos
        #De línea de comandos que son específicos de Qt o X11.
        #De la documentación oficial
        #https://doc.qt.io/qtforpython-6/tutorials/basictutorial/uifiles.html
        self.__app = QApplication(sys.argv)
        self.__window = Qt_ventana(self)
       
    def set_control(self,control):
        print('vista-control')
        self.__control = control
        self.__window.iniciar()
        #Asegura la correcta ejecución
        #De la documentación oficial
        sys.exit(self.__app.exec())
        
    def abrir(self,ruta):
        self.__control.cargar(ruta)
    
    def get_metadata(self):
        self.__control.get_metadata()

    def set_metadata(self,metadata):
        self.__window.desp_metadata(metadata)
        
    def filtro(self,clave):
        self.__control.filtro(clave)
    
    def filtro_valores(self,clave,valores):
        self.__control.filtro_valores(clave,valores)
        
    def desplegar(self,array):
        self.__window.desplegar(array)
    def eliminar(self):
        self.__control.eliminar()
    def error(self,clave,error):
        self.__window.error(clave,error)