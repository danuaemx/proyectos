#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 20:37:38 2024

@author: daniel
"""

from vista import Vista
from control import Control
from modelo import Modelo

 
if __name__ == '__main__':
    #MVC
    #Creación de la vista y modelo
    vista = Vista()
    modelo = Modelo()
    #Control tiene un modelo y una vista, relación
    control = Control(modelo,vista)
    #Se inicia el proceso principal
    control.iniciar()
    