#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cupy as cp
import numpy as np



def angulo(cpa, cpb):
    #Separar r,g,b
    cpa, cpb = cpa+1, cpb+1
    r ,g ,b =cpa[:,:,0],cpa[:,:,1], cpa[:,:,2]
    r1, g1, b1 =cpb[:,:,0], cpb[:,:,1], cpb[:,:,2]
    #Calcular coeficiente del angulo entre los dos vectores
    coef = (r1*r+g1*g+b1*b)/(cp.power(r1*r1+g1*g1+b1*b1,0.5)*cp.power(r*r+g*g+b*b,0.5))
    #Liberar memoria
    del r,g,b,r1,g1,b1
    coef = cp.stack([coef, coef, coef], axis=-1)
    #Si el angulo es 0 se da mayor ponderación
    #Si el angulo aumenta se da menor ponderación
    #Asegurar que no se tome en cuenta un blanco por sobreexposición
    cpan = (cpa+coef*cpb)/(1+coef)-1
    del coef
    return cpan

def hdr(*args):
    cpac,s = 0,0
    #Para cada box, chunk
    for cpa in args:
        #+1 por el 0
        cpa = cpa+1
        #Realiza Z con u=128 y sigma = 51
        #Ponderación de exposición
        cps = cp.exp(-1*cp.power(cpa-128,2)/(2*51*51))
        r ,g ,b =cps[:,:,0],cps[:,:,1],cps[:,:,2]
        del cps
        #Productorio de cada canal w= e_r*e_g*e_b
        saux = r*g*b
        del r,g,b
        r ,g ,b =cpa[:,:,0],cpa[:,:,1],cpa[:,:,2]
        #Calcula la distancia entre (r,g,b) y (g,b,r)
        cof = cp.power(r-g,2)+cp.power(g-b,2)+cp.power(b-r,2)
        del r,g,b
        #Debe ser entre 0 y 192
        cof = cp.clip(cof,64,192)
        #Multiplicación de los pesos
        saux = saux *cof
        del cof
        #Suma ponderada
        saux = cp.stack([saux, saux, saux], axis=-1)
        cpac = cpac+ saux*cpa
        del cpa
        #Normalización por total
        s = s+saux
        del saux
    #Va de 1 a 256 pero -1 es el rango válido
    #Obtiene los valores correctos
    cpac = cpac/s-1
    del s
    r ,g ,b =cpac[:,:,0],cpac[:,:,1],cpac[:,:,2]
    u = (r+g+b)/3
    del r,g,b
    #Calcula el promedio para centrar r'=r-u
    #Elimina más el azul
    u = cp.stack([u,u,1.2*u],axis=-1)
    cpac=2*cpac-u
    del u
    #Duda por pérdida de información
    #cpac = cp.clip(cpac,0,255)
    return cpac

#n de tamaño 1024,512,256,128
def hdr_cp(n,img_1,img_2,img_3,img_4):
    w,h,_ = img_1.shape
    #Más rápido en chunks cuadrados
    for y in range(0,h+1,n):
        for x in range(0,w+1,n):
            #Siempre menor que largo y ancho
            #Recortar las imagenes
            x1 = min(x+n,w-1)
            y1 = min(y+n,h-1)
            #Parece un hack, porque  son los mismos intervalos
            #expresado de otra forma y es más rápido sin razón aparente
            img1 = img_1[x:x1,y:y1,0:3]
            img2 = img_2[x:x1,y:y1,0:3]
            img3 = img_3[x:x1,y:y1,0:3]
            img4 = img_4[x:x1,y:y1,0:3]
            #Convertir a cupy
            cp1 = cp.array(img1,dtype= cp.float32)
            cp4 = cp.array(img4,dtype= cp.float32)
            #Pasar a ram y liberar memoria
            a = angulo(cp1,cp4)
            a_np = np.array(a.get(),dtype= np.float32)
            del cp1,cp4,a
            #Convertir a cupy
            cp2 = cp.array(img2,dtype= cp.float32)
            cp3 = cp.array(img3,dtype= cp.float32)
            #Pasar a ram y liberar memoria, no se requiere eliminar b aún
            b = angulo(cp2,cp3)
            del cp2,cp3
            #Convertir a cupy a, luego liberar memoria
            a= cp.array(a_np, dtype=cp.float32)
            hdri=hdr(a,b)
            del a,b
            hdri_np = np.array(hdri.get(),dtype= np.float32)
            del hdri
            #Para cada x se concatena
            if x == 0:
                hdrx = hdri_np
            else:
                hdrx = np.concatenate((hdrx,hdri_np),axis=0)
        #Para cada y se concatena
        if y == 0:
            hdrc = hdrx
        else:
            hdrc = np.concatenate((hdrc,hdrx),axis=1)
    return hdrc