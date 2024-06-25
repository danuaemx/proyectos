#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 20:37:15 2024

@author: daniel

Modelo extendido que integra kernels, matrices de transformación, etc.
"""

import numpy as np
from . import Modelo_core
from . algoritmos import brillo,contraste, log, expo, neg, promedio_est, centrar_est, bilinear_interpolation, eliminar_ran_hist, redim_hist,gris, trasl_ran_hist, mediana_filtro,erode, dilate, open, close, gradiente, eliminar_rostro, histograma_hexa
from PIL import Image
from.algoritmo_hdr_cupy import hdr_cp

class Modelo_data(Modelo_core):

    #Transformación de espacio del vector de intensidad
    def sepia(self):
        # Ingenuo elimina el azul y usa marrón, rojo, amarillo
        transf = [[255 / 573, 127 / 573, 255 / 573],
                  [63 / 573, 63 / 573, 255 / 573],
                  [0, 0, 0]]
        self.aplicar_transf(transf)

    def sepia1(self):
        #De internet
        transf = [[0.393, 0.769, 0.189],
                  [0.349, 0.686, 0.168],
                  [0.272, 0.534, 0.121]]
        self.aplicar_transf(transf)

    def sepia2(self):
        #Inspirado en sepia1
        transf = [[34 / 71, 46 / 71, 29 / 71],
                  [14 / 53, 23 / 53, 10 / 53],
                  [10 / 62, 13 / 62, 9 / 62]]
        self.aplicar_transf(transf)

    #Máscaras

    def promedio(self):
        kernel = [[.111, .111, .111],
                  [.111, .111, .111],
                  [.111, .111, .111]]
        self.aplicar(kernel)

    def blur(self):
        kernel = [[.0625, .125, .0625],
                  [.125, .25, .125],
                  [.0625, .125, .0625]]
        self.aplicar(kernel)

    def nitidez(self):
        kernel = [[0, -1, 0],
                  [-1, 5, -1],
                  [0, -1, 0]]
        self.aplicar(kernel)

    def definir(self):
        kernel = [[-.0625, -.125, -.0625],
                  [-.125, 1.75, -.125],
                  [-.0625, -.125, -.0625]]
        self.aplicar(kernel)

    def borde(self):
        kernel = [[-1, -1, -1],
                  [-1, 9, -1],
                  [-1, -1, -1]]
        self.aplicar(kernel)

    def nitidezl(self):
        kernel = [[-1, 0, -1],
                  [0, 5, 0],
                  [-1, 0, -1]]
        self.aplicar(kernel)

    def relieve(self):
        kernel = [[-1, -1, 1],
                  [-1, 1, 1],
                  [-1, 1, 1]]
        self.aplicar(kernel)

    def definir1(self):
        kernel = [[4, -1],
                  [-1, -1]]
        self.aplicar(kernel)
    
    def aplicar_transf_1(self, valores):
        norm, matriz = valores
        if norm:
            for i in range(matriz.shape[0]):
            # Calcular la suma del renglón
                suma_renglon = np.sum(matriz[i])
    
                # Si la suma es 0, evitar la división por cero cambiándola a 1
                if suma_renglon == 0:
                    suma_renglon = 1

                # Dividir el renglón por su suma
                matriz[i] /= suma_renglon
        self.aplicar_transf(matriz)

    def aplicar_mascara(self, valores):
        norm, valor = valores
        if norm:
            #Calcular la suma de los valores positivos y negativos
            suma_positivos = np.sum(valor[valor > 0])
            suma_negativos = -1*np.sum(valor[valor <= 0])
            #Si la suma es 0, evitar la división por cero cambiándola a 1
            if suma_positivos == 0:
                suma_positivos = 1
            if suma_negativos == 0:
                suma_negativos = 1
            #Si hay negativos, dividir los positivos por 0.5
            #Para evitar un resultado muy oscuro
            if suma_negativos > 0:
                valor[valor > 0] /= suma_positivos*0.5
            #Si no solo normalizar los positivos
            else:
                valor[valor > 0] /= suma_positivos
            valor[valor <= 0] /= suma_negativos

        self.aplicar(valor)

    #Edición sobre espacio color
    def hsv(self, valores):
        #Calcular HSV en formato PIL
        h, s, v = valores
        h = 255 * h / 360

        hsv_img = self._img.convert("HSV")
        aux_img = np.array(hsv_img).astype(np.float32)

        #Operación HSV
        aux_img[:, :, 0] += np.array([h])
        aux_img[:, :, 1:] *= np.array([s, v])

        self._modo = 'HSV'

        self.a_imagen(aux_img)

    def lab(self, valores):
        l, a, b = valores
        l = 255 * l / 100

        lab_img = self._img.convert("LAB")
        aux_img = np.array(lab_img).astype(np.float32)

        aux_img += np.array([l, a, b])

        self._modo = 'LAB'

        self.a_imagen(aux_img)

    def ruido_fft2_95(self):
        aux_img = self.ruido_fft2(self._img_aux, 0.05)
        self.a_imagen(aux_img)
    
    def ruido_fft2_90(self):
        aux_img = self.ruido_fft2(self._img_aux, 0.1)
        self.a_imagen(aux_img)

    def gaussian_4(self):
        aux_img = self.gaussian_n(self._img_aux.astype(np.float32), 4)
        self.a_imagen(aux_img)

    def gaussian_9(self):
        sigma = 9
        aux_img = self.gaussian_n(self._img_aux.astype(np.float32),
                                  sigma)
        self.a_imagen(aux_img)

    def bilateral402(self):
        aux_img = self.bilateral_nn1(self._img_aux.astype(np.float32),
                                     np.array(self._img.convert('L')).astype(np.float32),
                                     81,16)
        self.a_imagen(aux_img)
    
    def bilaterals(self):
        aux_img = self.bilateral_nn1(self._img_aux.astype(np.float32),
                                     np.array(self._img.convert('L')).astype(np.float32),
                                    16,9)
        self.a_imagen(aux_img)
    
    def bilateralc(self):
        aux_img = self.bilateral_nn1(self._img_aux.astype(np.float32),
                                     np.array(self._img.convert('L')).astype(np.float32),
                                    81,16)
        self.a_imagen(aux_img)
    
    def bilateral_custom(self, valores):
        sigma1,sigma2 = valores
        sigma1 = sigma1**2
        sigma2 = sigma2**2
        aux_img = self.bilateral_nn1(self._img_aux.astype(np.float32),
                                     np.array(self._img.convert('L')).astype(np.float32),
                                     sigma1,sigma2)
        self.a_imagen(aux_img)

    def mediana(self):
        aux_img = mediana_filtro(self._img_aux,3)
        self.a_imagen(aux_img)

    def mediana_amplio(self):
        aux_img = mediana_filtro(self._img_aux,9)
        self.a_imagen(aux_img)

    def erode_m(self):
        aux_img = erode(self._img_aux)
        self.a_imagen(aux_img)
    
    def dilate_m(self):
        aux_img = dilate(self._img_aux)
        self.a_imagen(aux_img)
    
    def open_m(self):
        aux_img = open(self._img_aux)
        self.a_imagen(aux_img)

    def close_m(self):
        aux_img = close(self._img_aux)
        self.a_imagen(aux_img)
    
    def grad_morf(self):
        aux_img = gradiente(self._img_aux,1)
        self.a_imagen(aux_img)
    
    def grad_neg_morf(self):
        aux_img = gradiente(self._img_aux,-1)
        self.a_imagen(aux_img)
    
    def open_close_morf(self):
        aux_img = open(self._img_aux)
        aux_img = close(aux_img)
        self.a_imagen(aux_img)
    
    def close_open_morf(self):
        aux_img = close(self._img_aux)
        aux_img = open(aux_img)
        self.a_imagen(aux_img)

    def ruido_fft2_c(self, valores):
        conf = valores
        conf = 1 - conf/100
        aux_img = self.ruido_fft2(self._img_aux, conf)
        self.a_imagen(aux_img)
    def cop(self, valores):
        p, shape, p1 = valores
        aux_img = self.copiado_circ(p,shape,p1)
        self.a_imagen(aux_img)
    
    def del_roi(self, valores):
        p, shape = valores
        img_aux = self.del_circle(p,shape)
        self.a_imagen(img_aux)
    
    def redim(self, valores):
        ancho,alto = valores
        resultado = np.zeros((alto,ancho,3)).astype(np.float32)
        resultado = bilinear_interpolation(self._img_aux,ancho,alto,resultado)
        self.a_imagen(resultado)
    
    def crop_rect(self, valores):
        x1,y1,x2,y2 = valores
        img = self._img_aux[y1-1:y2,x1-1:x2]
        self.a_imagen(img)

    #No se requiere modelo core
    def brillo(self, valores):
        aux_img = brillo(self._img_aux.astype(np.float32),
                        np.array(valores).astype(np.float32))
        self.a_imagen(aux_img)
    
    def contraste(self, valores):
        aux_img = contraste(self._img_aux.astype(np.float32),
                          np.array(valores).astype(np.float32))
        self.a_imagen(aux_img)
    
    def logaritmo(self, valores):
        aux_img = log(self._img_aux.astype(np.float32),
                        #C
                      np.array(valores[0]).astype(np.float32),
                        #C0
                      np.array(valores[1]).astype(np.float32))
        self.a_imagen(aux_img)
    
    def exponencial(self, valores):
        aux_img = expo(self._img_aux.astype(np.float32),
                       #C
                       np.array(valores[0]).astype(np.float32),
                       #Exponente
                       np.array(valores[1]).astype(np.float32),
                       #C0
                       np.array(valores[2]).astype(np.float32))
        self.a_imagen(aux_img)
    
    def negativo(self):
        aux_img = neg(self._img_aux.astype(np.float32))
        self.a_imagen(aux_img)
    
    def espejo_h(self):
        aux_img = np.fliplr(self._img_aux)
        self.a_imagen(aux_img)
    
    def espejo_v(self):
        aux_img = np.flipud(self._img_aux)
        self.a_imagen(aux_img)

    def rotar90(self):
        aux_img = np.rot90(self._img_aux)
        self.a_imagen(aux_img)
    
    def rotar_90neg(self):
        aux_img = np.rot90(self._img_aux,3)
        self.a_imagen(aux_img)
    
    def promedio_f(self):
        aux_img = promedio_est(self._img_aux)
        self.a_imagen(aux_img)
    
    def centrar_f(self):
        aux_img = centrar_est(self._img_aux)
        self.a_imagen(aux_img)

    def ecualizar(self):
        aux_img = self.get_ecualizar()
        self.a_imagen(aux_img)
    
    def del_ran_hist(self, valores):
        min,max = valores
        aux_img = eliminar_ran_hist(np.clip(self._img_aux,0,255),min,max)
        self.a_imagen(aux_img)
    
    def comp_exp(self, valores):
        x1,x2 = valores
        gris_aux = np.clip(gris(np.copy(self._img_aux)),0,255)
        min = np.min(self._img_aux)
        max = np.max(self._img_aux)
        aux_img = redim_hist(self._img_aux,x1,x2,min,max,gris_aux)
        aux_img = np.clip(aux_img,x1,x2)
        self.a_imagen(aux_img)
    
    def cop_hist(self, valores):
        x1,x2,n1,n2 = valores
        gris_aux = np.clip(gris(np.copy(self._img_aux)),0,255)
        print(x1,x2,n1,n2)
        aux_img= trasl_ran_hist(self._img_aux,x1,x2,n1,n2,gris_aux)
        self.a_imagen(aux_img)

    def del_rostro(self, valores):
        img_aux = np.copy(self._img_aux)
        aux = self.get_ecualizar()
        y,x,c = aux.shape
        aux = bilinear_interpolation(aux,x//10,y//10,np.zeros((y//10,x//10,c)).astype(np.float32))
        aux = open(close(aux))
        aux = eliminar_rostro(valores[0]//10,valores[1]//10,aux,img_aux)
        self.a_imagen(aux)

    def hdr_a(self,valores):
        dir1,dir2,dir3,dir4 = valores
        img1 = np.array(Image.open(dir1)).astype(np.float32)
        img2 = np.array(Image.open(dir2)).astype(np.float32)
        img3 = np.array(Image.open(dir3)).astype(np.float32)
        img4 = np.array(Image.open(dir4)).astype(np.float32)
        #Máximo soportado por mi GPU 1024*1024
        try:
            aux_img = hdr_cp(1024,img1,img2,img3,img4)
            self.a_imagen(aux_img)
        except:
            aux_img = hdr_cp(512,img1,img2,img3,img4)
            self.a_imagen(aux_img)
    
    def reconst_ruido(self):
        self._img_aux = self.ruido_fft2(self._img_aux, 0.1)
        self._img_aux= mediana_filtro(self._img_aux,9)
        self.a_imagen(self._img_aux)
        self._img_aux = self.bilateral_nn1(self._img_aux.astype(np.float32),
                                     np.array(self._img.convert('L')).astype(np.float32),
                                    16,9)
        self.nitidez()

    def ruido_nocturno(self):
        self._img_aux = self.bilateral_nn1(self._img_aux.astype(np.float32),
                                     np.array(self._img.convert('L')).astype(np.float32),
                                    81,16)
        self._img_aux = close(self._img_aux)
        self._img_aux = open(self._img_aux)
        self._img_aux = gradiente(self._img_aux,-1)
        self.a_imagen(self._img_aux)
    
        

