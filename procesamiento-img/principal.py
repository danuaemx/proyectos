#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 20:37:38 2024

Este archivo contiene la clase Main que representa el punto de entrada del programa.
"""

from vista import Vista
from control import Control 
from modelo import Modelo
from multiprocessing import Process


class Main(Process):

    def __init__(self):
        """
        Inicializa una nueva instancia de la clase Main.
        """
        Process.__init__(self)
        self.__control = None
        self.__modelo = None
        self.__vista = None

    def run(self):
        """
        Método run override que se ejecuta cuando se inicia el proceso.
        Crea instancias de la vista, el modelo y el controlador,
        y luego inicia el controlador.
        """
        self.__vista = Vista()
        self.__modelo = Modelo()
        self.__control = Control(self.__modelo, self.__vista)
        self.__control.iniciar()


if __name__ == '__main__':
    proceso = Main()
    proceso.start()
    proceso.join()
    # Si se cierra la ventana principal, se cierra el programa
    raise SystemExit
