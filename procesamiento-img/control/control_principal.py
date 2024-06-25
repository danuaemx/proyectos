#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 20:36:04 2024

Este módulo contiene la clase Control que se encarga de controlar la interacción entre el modelo y la vista en una aplicación GUI.

La clase Control tiene los siguientes métodos:

- __init__(self, modelo, vista): Constructor de la clase Control que recibe una instancia del modelo y una instancia de la vista.
- iniciar(self): Método que inicializa el controlador y establece la relación entre el modelo y la vista.
- cargar(self, ruta): Método que carga un archivo en el modelo en un hilo separado.
- filtro(self, clave): Método que realiza un filtro en el modelo en un hilo separado.
- filtro_valores(self, clave, valores): Método que realiza un filtro con valores específicos en el modelo en un hilo separado.
- desp(self, array): Método que despliega un np.darray en la vista en un hilo separado.
- guardar(self, ruta): Método que guarda el modelo en un archivo en un hilo separado.
- eliminar(self): Método que elimina el modelo en un hilo separado.
"""

from threading import Thread
import time
import logging
from datetime import datetime

class Control:

    def __init__(self, modelo, vista):
        self.__modelo = modelo
        self.__vista = vista

    def iniciar(self):
        print('control set')
        
        #Registro de uso de la aplicación
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nombre_archivo_log = f"control/.log/debug_{timestamp}.log"
        logging.basicConfig(filename=nombre_archivo_log, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info('Se ha iniciado una instancia')
        
        self.__modelo.set_control(self)
        self.__vista.set_control(self)

    def cargar(self, ruta):
        try:
            time_0 = time.time()
            thread = Thread(target=self.__modelo.abrir, args=(ruta,))
            thread.start()
            thread.join()
            time_1 = time.time()-time_0
            logging.info(f'cargar tardó {time_1}')
        except Exception as e:
            logging.error(f'Error en cargar: {e}')
            self.__vista.error('cargar', e)

            

    def filtro(self, clave):
        try:
            time_0 = time.time()
            thread = Thread(target=self.__modelo.filtro, args=(clave,))
            thread.start()
            thread.join()
            time_1 = time.time()-time_0
            #print(f'{clave} tardó {time_1}')
        except Exception as e:
            logging.error(f'Error en filtro {clave}: {e}')
            self.__vista.error(clave, e)

    def filtro_valores(self, clave, valores):
        try:
            time_0 = time.time()
            thread = Thread(target=self.__modelo.filtro_valores, args=(clave, valores))
            thread.start()
            thread.join()
            time_1 = time.time()-time_0
            #print(f'{clave} tardó {time_1}')
        except Exception as e:
            logging.error(f'Error en filtro_valores({valores})) {clave}: {e}')
            self.__vista.error(clave, e)

    def desp(self, array):

        try:
            time_0 = time.time()
            thread = Thread(target=self.__vista.desplegar, args=(array,))
            thread.start()
            thread.join()
            time_1 = time.time()-time_0
            logging.info(f'desplegar tardó {time_1}')
        except Exception as e:
            logging.error(f'Error en desplegar: {e}')
            self.__vista.error('desplegar', e)
        
    def guardar(self, ruta):
        try:
            time_0 = time.time()
            thread = Thread(target=self.__modelo.guardar, args=(ruta,))
            thread.start()
            thread.join()
            time_1 = time.time()-time_0
            logging.info(f'guardar {ruta} tardó {time_1}')
        except Exception as e:
            logging.error(f'Error en guardar: {e}')
            self.__vista.error('guardar', e)

    def eliminar(self):
        try:
            time_0 = time.time()
            thread = Thread(target=self.__modelo.eliminar)
            thread.start()
            thread.join()
            time_1 = time.time()-time_0
            logging.info(f'Se ha cerrado en {time_1}')
        except Exception as e:
            logging.error(f'Error en eliminar: {e}')
            self.__vista.error('eliminar', e)
    
    def get_metadata(self):
        try:
            self.__modelo.get_metadata()
        except Exception as e:
            logging.error(f'Error en eliminar: {e}')
            self.__vista.error('eliminar', e)
    
    def set_metadata(self,metadata):
        try:
           self.__vista.set_metadata(metadata)
        except Exception as e:
            logging.error(f'Error en eliminar: {e}')
            self.__vista.error('eliminar', e)