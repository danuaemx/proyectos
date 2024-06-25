#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 20:54:59 2024

@author: daniel

Integra los diccionarios de funciones
"""

from . import Modelo_data


class Modelo(Modelo_data):

    def __init__(self):
        super().__init__()
        self.__dict = None
        self.__dict1 = None

    def filtro(self, clave):
        self.__dict = {#Máscaras
                       "promedio": self.promedio,
                       "nitidez": self.nitidez,
                       "blur": self.blur,
                       "definir": self.definir,
                       "borde": self.borde,
                       "nitidezl": self.nitidezl,
                       "relieve": self.relieve,
                       "definir1": self.definir1,
                       #Colores
                       "sepia1": self.sepia,
                       "sepia2": self.sepia1,
                       "sepia3": self.sepia2,
                       "negativo": self.negativo,
                       #Ruido
                       "ruido_fft2_95": self.ruido_fft2_95,
                       "ruido_fft2_90": self.ruido_fft2_90,
                       "gaussian_4": self.gaussian_4,
                       "gaussian_9": self.gaussian_9,
                       "bilaterals": self.bilaterals,
                       "bilateralc": self.bilateralc,
                       "mediana": self.mediana,
                       "mediana_amplio": self.mediana_amplio,
                       #Avanzado
                       "bilateral402": self.bilateral402,
                       #Espacial
                       "espejo_v": self.espejo_v,
                       "espejo_h": self.espejo_h,
                       'rotar90': self.rotar90,
                       'rotar90neg': self.rotar_90neg,
                       #Control
                       "deshacer": self.deshacer,
                       "rehacer": self.rehacer,
                       #Frecuencua
                       "promedio_f": self.promedio_f,
                       "centrar_f": self.centrar_f,
                       "ecualizar": self.ecualizar,
                       #Morfológicos
                       'erode': self.erode_m,
                        'dilate': self.dilate_m,
                        'open': self.open_m,
                        'close': self.close_m,
                        'grad_morf': self.grad_morf,
                        'grad_neg_morf': self.grad_neg_morf,
                        'open_close_morf': self.open_close_morf,
                        'close_open_morf': self.close_open_morf,
                        #Avanzado
                        'huffman': self.huffman,
                        'reconst_ruido': self.reconst_ruido,
                        'ruido_nocturno': self.ruido_nocturno,
                       }

        self.__dict[clave]()

    def filtro_valores(self, clave, valores):
        self.__dict1 = {#Colores
                        'hue':self.hsv,
                        'sat': self.hsv,
                        'val': self.hsv,
                        'lum': self.lab,
                        'a': self.lab,
                        'b': self.lab,
                        'brillo': self.brillo,
                        'contraste': self.contraste,
                        'log': self.logaritmo,
                        'exponencial': self.exponencial,
                        'transf_custom': self.aplicar_transf_1,
                        'mask_custom': self.aplicar_mascara,
                        #Espacial
                        'cop': self.cop,
                        'eliminar_roi': self.del_roi,
                        'redim': self.redim,
                        'crop_rect': self.crop_rect,

                        #Ruido
                        'ruido_fft2': self.ruido_fft2_c,
                        'bilateral_custom': self.bilateral_custom,

                        #Frecuencia
                        'del_ran_hist': self.del_ran_hist,
                        'com_exp': self.comp_exp,
                        'cp_sel_hist': self.cop_hist,

                        #Avanzado
                        'del_rostro': self.del_rostro,
                        'modo_L': self.modo_L,
                        'hdr': self.hdr_a,
                        #Guardar
                        'guardar': self.guardar,
                        }

        self.__dict1[clave](valores)
