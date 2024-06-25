#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 20:36:34 2024

@author: daniel

Modelo núcleo que sólo integra algrítmos básicos y no puede realizar operaciones
"""

from PIL import Image
from PIL.ExifTags import TAGS
import numpy as np
import os
import glob
from .algoritmos import transf1, conv, gaussian, ruido_fft2_o, bilateral_gauss, cp_roi, gris, histograma, ecualizar_map, del_roi_circ,histograma_hexa
import dahuffman as hf
class Modelo_core:

    def __init__(self):
        #Para saber que atributos se tienen
        self._modo = None
        self._control = None
        self._img = None
        self._contador = 0
        #Para los archivos temporales
        self._img: Image
        self._img_aux: np.ndarray
        self._modo: str

    def set_control(self, control):
        self._control = control
        print('modelo-control')
        #Para el modo HSV, LAB, RGB
        self._modo = 'RGB'
    
    
    def abrir(self, ruta):
        #Convierte a RGB de 24-bits por pixel (Caso L)
        if ruta.endswith('.immi'):
            self.immi_load(ruta[:-5])
            return
        else:
            self._img = Image.open(ruta).convert("RGB")
            #Obtener metadata
            self._modo = 'RGB'
            #Requerido para para flotante de 32-bits
            self._img_aux = np.array(self._img).astype(np.float32)
            #La imagen se despliega de manera incorrecta
            metadata = [f'{self._img_aux.shape[0]}x{self._img_aux.shape[1]}',]
            tag_list = ['dimensiones']
            try:
                exif_data = Image.open(ruta).getexif()
                if exif_data:
                    
                    for tag, value in exif_data.items():
                        tag_name = TAGS.get(tag, tag)
                        # Filtrar datos binarios y mostrar solo texto legible
                        if isinstance(value, bytes):
                            continue  # Ignorar datos binarios
                        if isinstance(value, str) or isinstance(value, int) or isinstance(value, float):
                            metadata.append(value)
                            tag_list.append(tag_name)
            except:
                pass

            self.__metadata = [tag_list,metadata]
            self.a_imagen(self._img_aux)
            #self._control.desp(np.flipud(np.rot90(self._img_aux)))

    def guardar(self, valores):
        ruta,formato,color = valores
        ruta_imi = ruta
        ruta = f'{ruta}.{formato}'
        if color == 'CMYK' and formato == 'TIFF':
            self._img = self._img.convert('CMYK')
            self._img.save(ruta,compression='tiff_lzw')
        elif color == 'RGB' and formato in ['JPEG','PNG','TIFF','BMP']:
            self._img.save(ruta)
        elif color == 'RGB' and formato == 'IMMI':
            self.huffman(ruta_imi)
        

    def modo_L(self,img):
        #Si esta en modo L (desctivar)
        if self._modo == 'L':
            self._modo = 'RGB'
            img = np.flipud(np.rot90(img,k=1))
            self.a_imagen(img.astype(np.float32))
        #Si se cambia el modo
        else:
            self._modo = 'L'
            #Se trabaja a tres canales
            self.img_aux = gris(self._img_aux)
            #Para desplegar y guardar
            self.a_imagen(self._img_aux.astype(np.float32))
    
    def deshacer(self):
        try:
            #Se carga la imagen anterior
            self._img_aux = np.load(f'.tmp/img{self._contador-2}.npy')
            self._img = Image.fromarray(np.clip(self._img_aux, 0, 255).astype(np.uint8))
            self._contador -= 1
            #Desplegar
            self._control.desp(np.flipud(np.rot90(np.clip(self._img_aux,0,255)).astype(np.uint8)))
        except FileNotFoundError:
            pass

    def rehacer(self):
        try:
            #Se carga la imagen anterior
            self._img_aux = np.load(f'.tmp/img{self._contador}.npy')
            self._img = Image.fromarray(np.clip(self._img_aux, 0, 255).astype(np.uint8))
            #Desplegar
            self._contador += 1
            self._control.desp(np.flipud(np.rot90(np.clip(self._img_aux,0,255)).astype(np.uint8)))
        except FileNotFoundError:
            pass

    #Método que despliega y guarda archivo temporal.    
    def a_imagen(self, img_aux):
        no_calc = True

        #Modo HSV
        if self._modo == 'HSV':
            self._img = Image.fromarray(np.clip(img_aux, 0, 255).astype(np.uint8), "HSV").convert("RGB")
            #Desactiva el modo L por la naturaleza del cambio
            self._modo = 'RGB'
            img_aux = np.array(self._img)
            no_calc = False

        #Modo LAB
        if self._modo == 'LAB':
            self._img = Image.fromarray(np.clip(img_aux, 0, 255).astype(np.uint8), "LAB").convert("RGB")
            #Desactiva el modo L por la naturaleza del cambio
            self._modo = 'RGB'
            img_aux = np.array(self._img)
            no_calc = False

        #En modos HSV Y LAB se precalcula la imagen PIL
        #Si se usa mode hay repetición por el cambio en LAB Y HSV
        if no_calc:
            self._img = Image.fromarray(np.clip(img_aux, 0, 255).astype(np.uint8))

        #Valores se garantiza una imagen con valores mas allá de 255 o menos de 0
        #No se pierde información valiosa, excepto en HSV, LAB y modo L (Pendiente HSV, LAB)
        #PIL no recomendable en procesamiento de imágenes
        #el hecho de que trabaja con 8-bits hace que pierda información
        self._img_aux = img_aux.astype(np.float32)

        ruta = f'.tmp/img{self._contador}.png'
        self._img.save(ruta)
        ruta_np = f'.tmp/img{self._contador}.npy'
        np.save(ruta_np, self._img_aux)
        self._contador += 1

        #Modo despliegue valores entre 0 y 255 eficiencia por np.uint8
        if self._modo == 'L':
            self._control.desp(np.flipud(np.rot90(np.clip(self._img_aux[:, :, 0],0,255))).astype(np.uint8))
        else:
            self._control.desp(np.flipud(np.rot90(np.clip(self._img_aux,0,255))).astype(np.uint8))

    # Matriz*vector_I    
    def aplicar_transf(self, transf):
        # a np objeto
        np_img = self._img_aux.astype(np.float32)
        transf_np = np.array(transf).astype(np.float32)
        salida = np.empty_like(np_img).astype(np.float32)
        # tranformar
        img_aux = transf1(np_img, salida, transf_np)
        # guardar
        self.a_imagen(img_aux)

    #Máscara
    def aplicar(self, kernel):
        #A np objeto
        np_img = self._img_aux.astype(np.float32)
        kernel_np = np.array(kernel).astype(np.float32)
        salida = np.empty_like(np_img).astype(np.float32)
        img_aux = conv(np_img, kernel_np, salida)

        #Guardar
        self.a_imagen(img_aux)

    def ruido_fft2(self, img, conf):
        return ruido_fft2_o(img, conf)
    
    #Aplica el gaussiano y lo regresa
    def gaussian_n(self, img, sigma):
        n = np.round(np.sqrt(sigma) * 3).astype(np.int32)
        g = np.zeros((2*n,2*n))
        img_filtrada = np.empty_like(img)
        return gaussian(img, sigma,g,n,img_filtrada)
    
    #Bilateral
    def bilateral_nn1(self, img, img_l, sigma1, sigma2):
        img_filtrada = np.empty_like(img)
        n = np.round(np.sqrt(sigma1)* 3).astype(np.int32)
        g = np.zeros((2*n,2*n))
        return bilateral_gauss(img, img_l, sigma1, sigma2,g,n,img_filtrada)
    
    #Copiado circular
    def copiado_circ(self,p,shape,p1):
        p_r = np.round(p+1).astype(np.int32)
        shape_r = np.round(shape/2).astype(np.int32)
        p1_r = np.round(p1).astype(np.int32)+shape_r
        o = p_r+shape_r
        r = shape_r[0]
        return cp_roi(self._img_aux,r,o[1],o[0],p1_r[1],p1_r[0])
    
    def del_circle(self,p,shape):
        p_r = np.round(p+1).astype(np.int32)
        shape_r = np.round(shape/2).astype(np.int32)
        o = p_r+shape_r
        r = shape_r[0]
        return del_roi_circ(self._img_aux,r,o[1],o[0])
    
    def get_ecualizar(self):
        img_gris = np.copy(self._img_aux).astype(np.float32)
        img_gris = np.clip(img_gris, 0, 255)
        img_gris = gris(img_gris).astype(np.uint8)

        hist =  histograma(img_gris)
        #Contiene la posición de cada valor en el histograma normalizado
        #hist[n] = pos_n de 0 a 255
        tot = np.sum(hist)
        ac = 0
        hist_pos_n = np.zeros(len(hist))
        for x in range(len(hist)):
            val = hist[x]
            ac += val
            hist_pos_n[x] =  255*ac
        hist_pos_n = (hist_pos_n/tot).astype(np.int32)
        img_aux = ecualizar_map(self._img_aux,hist_pos_n,img_gris)
        return img_aux
    def get_metadata(self):
        self._control.set_metadata(self.__metadata)
    #Eliminar temporales
    def eliminar(self):
        carpeta = '.tmp'
        # Construir el patrón de búsqueda para archivos de imagen
        patron = os.path.join(carpeta, '*.png')

        # Obtener la lista de archivos de imagen
        archivos_imagen = glob.glob(patron)

        # Eliminar cada archivo de imagen encontrado
        for archivo in archivos_imagen:
            try:
                os.remove(archivo)
            except OSError as e:
                print(e)
        
        patron = os.path.join(carpeta, '*.npy')
        archivos_imagen = glob.glob(patron)
        for archivo in archivos_imagen:
            try:
                os.remove(archivo)
            except OSError as e:
                print(e)
    
    def immi_load(self,dir):
        #Cargar la tabla de frecuencias
        self._codec = hf.HuffmanCodec.load(f'{dir}.huf')
        #Cargar la imagen comprimida
        with open(f'{dir}.immi', 'rb') as f:
            encode = f.read()
        #Cargar las dimensiones de la imagen
        with open(f'{dir}.shp', 'rb') as f:
            shape = f.read().decode().split('\t')
        #Convertir las dimensiones a enteros
        shape = [int(i) for i in shape]
        #Decodificar la imagen
        decode = self._codec.decode(encode)
        #Crear la imagen vacía
        img1 = np.zeros((shape[0],shape[1],shape[2])).astype(np.uint8)
        i = 0 
        #Recorrer la imagen y agregar cada pixel a la imagen
        for a in range (shape[0]):
            for b in range (shape[1]):
                for c in range (shape[2]):
                    if i == len(decode):
                        break
                    img1[a,b,c] = ord(decode[i])
                    i += 1
        #Desplegar la imagen
        self.a_imagen(img1)

    def huffman_compresion(self,ruta):
        #Formato de la imagen de 3 canales y 8 bits por canal
        img = np.clip(self._img_aux,0,255).astype(np.uint8)
        #Iniciar la cadena de bytes
        hex_string = ''
        #Recorrer la imagen y agregar cada pixel a la cadena
        for a in range (img.shape[0]):
            for b in range (img.shape[1]):
                for c in range (img.shape[2]):
                    hex_string += chr(img[a,b,c])
        #Codificar la cadena con el codec
        encoded = self._codec.encode(hex_string)
        #Guardar la imagen comprimida
        with open(f'{ruta}.immi', 'wb') as f:
            f.write(encoded)
        #Guardar la tabla de frecuencias
        self._codec.save(f'{ruta}.huf')
        #Guardar las dimensiones de la imagen
        with open(f'{ruta}.shp', 'wb') as f:
            f.write(f'{img.shape[0]}\t{img.shape[1]}\t{img.shape[2]}'.encode())
        
        #Análisis de la compresión
        print(f'Original: {len(hex_string)}')
        print(f'Comprimido: {len(encoded)}')
        print(f'Ratio: {len(encoded)/len(hex_string)}')
                    
    def huffman_hist(self,hist,ruta):
        dict = {chr(i):hist[i] for i in range(len(hist)) if hist[i] > 0}
        self._codec = hf.HuffmanCodec.from_frequencies(dict)
        self.huffman_compresion(ruta)
      
    def huffman(self,ruta):
        hist = histograma_hexa(np.clip(self._img_aux,0,255).astype(np.uint8))
        self.huffman_hist(hist,ruta)
