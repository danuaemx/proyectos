# -*- coding: utf-8 -*-
import numpy as np
import scipy as sc
from numba import jit


@jit(nopython=True)
def gris(img):
    #Convertir a escala de grises
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            #Suma ponderada
            img[i, j] = 0.299 * img[i, j, 0] + 0.587 * img[i, j, 1] + 0.114 * img[i, j, 2]
    return img

@jit(nopython=True)
def neg(img):
    #Negativo de la imagen
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):
                img[i, j, k] = 255 - img[i, j, k]
    return img

@jit(nopython=True)
def expo(img, c,exps,c_0):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):
                #C*e^(exps*img)+c_0
                img[i, j, k] = c*np.exp(img[i, j, k]*exps)+c_0
    return img

@jit(nopython=True)
def log(img, c,c_0):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):
                #C*log(1+img)+c_0
                img[i, j, k] = c*np.log(1+img[i, j, k])+c_0
    return img

@jit(nopython=True)
def brillo(img, valor):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):
                #Sumar valor
                img[i, j, k] = img[i, j, k]+valor
    return img

@jit(nopython=True)
def contraste(img, valor):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):
                #Multiplicar por valor
                img[i, j, k] = valor*img[i, j, k]
    return img

@jit(nopython=True)
#Por alguna razón np.sum es más lento en este contexto
def transf1(img, salida, transf):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):
                salida[i, j, k] = img[i, j, 0] * transf[k, 0] + img[i, j, 1] * transf[k, 1] + img[i, j, 2] * transf[
                    k, 2]
                #np.sum(img[i, j, :] * transf[k, :])

    return salida


def conv(img, knl, salida):
    #Convolución usando transformada rápida de Fourier
    for dim in range(3):
        salida[:, :, dim] = sc.signal.fftconvolve(img[:, :, dim],
                                                  knl,
                                                  mode='same')
    return salida


@jit(nopython=True)
def gaussian(img, sigma,g,n,img_filtrada):
    #De https://cs.brown.edu/courses/csci1290/labs/lab_bilateral/index.html 
    #Implementación numba
    #min y max no definidas
    #Usa empty_like
    sigma1 = 2 * sigma * sigma
    largo, alto, bandas = img.shape
    
    #Para eficiencia
    #Calcular kernel
    w_t=0
    for i in range(0, 2*n):
        for j in range(0,2*n):
            g[j,i]= np.exp( -(i*i +j*j)/sigma1)
            w_t += g[j,i]
    
    # Iterar sobre pixeles       
    for y in range(largo):
        for x in range(alto):
            w = w_t
            gp = np.array([0, 0, 0])
            # Iterar sobre el kernel
            for i in range(-n, n):
                for j in range(-n, n):
                    q_x, q_y = x + j, y + i
                    jj,ii = j+n,i+n
                    #Clip para que no se salga del rango
                    #Quitamos el peso no usado para normalizar
                    if q_y > largo - 1:
                        w -= g[jj,ii]
                    elif q_x> alto - 1:
                        w -= g[jj,ii]
                    elif 0 > q_y:
                        w -= g[jj,ii]
                    elif 0 > q_x:
                        w -= g[jj,ii]
                    else:
                        # Filtro g = Z(r^2) con desviación de sigma
                        #gp += g * img[q_y, q_x, :]
                        for banda in range(bandas):
                            # Acumular por el pixel
                            gp[banda] += g[jj,ii] * img[q_y,q_x, banda]

            #p=G(p)/w, normalizado +1 por si es 0, -1 para que quede entre 255
            img_filtrada[y, x, :] = (gp + 1)/(w + 1) - 1

    return img_filtrada


@jit(nopython=True)
#Se precalcula I
def bilateral_gauss(img, img_L, sigma, sigma1,g,n,img_filtrada):
    #Implementación numba
    #min y max no definidas
    #Usa empty_like
    
    largo, alto, bandas = img.shape
    
    sigma00 = 2 * sigma * sigma
    sigma11 = 2 * sigma1 * sigma1
    
    for i in range(0, 2*n):
        for j in range(0,2*n):
            g[j,i]= np.exp( -(i*i +j*j)/sigma00)
    # Iterar sobre pixeles       
    for y in range(largo):
        for x in range(alto):
            w=0
            gp = np.array([0, 0, 0])
            # Iterar sobre el kernel
            for i in range(-n, n):
                for j in range(-n, n):
                    q_x, q_y = x + j, y + i
                    jj,ii = j+n,i+n
                    #Clip para que no se salga del rango
                    #Quitamos el peso no usado para normalizar
                    if q_y > largo - 1:
                        pass
                    elif q_x> alto - 1:
                        pass
                    elif 0 > q_y:
                        pass
                    elif 0 > q_x:
                        pass
                    else:
                        gg = g[jj,ii]*np.exp(-(img_L[q_y, q_x] - img_L[y, x]) * (img_L[q_y, q_x] - img_L[y, x]) / sigma11)
                        w+=gg
                        # Filtro g = Z(r^2) con desviación de sigma
                        #gp += g * img[q_y, q_x, :]
                        for banda in range(bandas):
                            # Acumular por el pixel
                            gp[banda] += gg*img[q_y,q_x, banda]

            #p=G(p)/w, normalizado +1 por si es 0, -1 para que quede entre 255     
                img_filtrada[y, x, :] = (gp + 1)/(w + 1) - 1

    return img_filtrada
    
@jit(nopython=True)
def cp_roi(img,r,o_x,o_y,f_x,f_y):
    for x in range(-r,r+1):
        for y in range(-r,r+1):
            d_r = x*x+y*y-r*r
            if d_r<-1:
                img[x+f_x,y+f_y,:]=img[x+o_x,y+o_y,:]
    return img

@jit(nopython=True)
def del_roi_circ(img,r,o_x,o_y):
    for x in range(-r,r+1):
        for y in range(-r,r+1):
            d_r = x*x+y*y-r*r
            if d_r<-1:
                img[x+o_x,y+o_y,:]=np.array([0,0,0])
    return img

@jit(nopython=True)
def promedio_est(img):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            u = (img[i, j, 0] + img[i, j, 1] + img[i, j, 2])/3
            u = np.array([u, u, u])
            img[i, j,:] = 1.5*img[i, j, :] - 0.5*u
    return img

@jit(nopython=True)
def centrar_est(img):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            u = (img[i, j, 0] + img[i, j, 1] + img[i, j, 2])/3
            u = np.array([u, u, u])
            img[i, j,:] = (img[i, j, :] + 0.5*u)/1.5
    return img

@jit(nopython=True)
def histograma(img):
    #Histograma de la imagen que en rangon 0 a ?
    hist = np.zeros(256)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
                #Asegurar que se pueda usar como índice
                a = img[i, j].astype(np.int32)
                hist[a] += 1
    return hist

@jit(nopython=True)
def ecualizar_map(img,hist_pos_n,img_gris):
    #Ecualiza la imagen
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            pos = img_gris[i, j]
            map = hist_pos_n[pos]
            if np.any(pos) == 0:
                r = (map+1)/(pos+1)
            else:
                r = map/pos
            for k in range(3):
                img[i, j,k] = (r*img[i, j,k])[0]
    return img

def erode(img):
    erode_r = sc.ndimage.grey_erosion(img[:,:,0], size=(3,3))
    erode_g = sc.ndimage.grey_erosion(img[:,:,1], size=(3,3))
    erode_b = sc.ndimage.grey_erosion(img[:,:,2], size=(3,3))
    erode = np.dstack((erode_r, erode_g, erode_b))
    return erode

def dilate(img):
    dilate_r = sc.ndimage.grey_dilation(img[:,:,0], size=(3,3))
    dilate_g = sc.ndimage.grey_dilation(img[:,:,1], size=(3,3))
    dilate_b = sc.ndimage.grey_dilation(img[:,:,2], size=(3,3))
    dilate = np.dstack((dilate_r, dilate_g, dilate_b))
    return dilate

def open(img):
    open_r = sc.ndimage.grey_opening(img[:,:,0], size=(3,3))
    open_g = sc.ndimage.grey_opening(img[:,:,1], size=(3,3))
    open_b = sc.ndimage.grey_opening(img[:,:,2], size=(3,3))
    open = np.dstack((open_r, open_g, open_b))
    return open

def close(img):
    close_r = sc.ndimage.grey_closing(img[:,:,0], size=(3,3))
    close_g = sc.ndimage.grey_closing(img[:,:,1], size=(3,3))
    close_b = sc.ndimage.grey_closing(img[:,:,2], size=(3,3))
    close = np.dstack((close_r, close_g, close_b))
    return close

def gradiente(img,r):
    grad_r = sc.ndimage.morphological_gradient(img[:,:,0], size=(3,3))
    grad_g = sc.ndimage.morphological_gradient(img[:,:,1], size=(3,3))
    grad_b = sc.ndimage.morphological_gradient(img[:,:,2], size=(3,3))
    grad = img+0.5*r*np.dstack((grad_r, grad_g, grad_b))
    return grad


def mediana_filtro(img,r):
    #Filtro de mediana
    mediana_r = sc.ndimage.median_filter(img[:,:,0], r)
    mediana_g = sc.ndimage.median_filter(img[:,:,1], r)
    mediana_b = sc.ndimage.median_filter(img[:,:,2], r)
    mediana = np.dstack((mediana_r, mediana_g, mediana_b))
    #Aplicar ratio a cada canal
    return mediana

def ruido_fft2_o(img, conf):
    #Complemento del conjunto usado en:
    #https://scipy-lectures.org/intro/scipy/auto_examples/solutions/plot_fft_image_denoise.html
    #Podría ser igual, pero no.
    #Conf es fft_S/fft_T con respecto al ruido (valores centrales)
    x, y, z = img.shape
    cmp = np.empty_like(img)
    for dim in range(z):
        img_fft = sc.fftpack.fft2(img[:, :, dim])

        img_fft[:int(x * conf), :int(y * conf)] = 0
        img_fft[:int(x * conf), int(y * (1 - conf)):] = 0
        img_fft[int(x * (1 - conf)):, :int(y * conf)] = 0
        img_fft[int(x * (1 - conf)):, int(y * (1 - conf)):] = 0

        cmp[:, :, dim] = sc.fftpack.ifft2(img_fft).real

    return img - cmp

@jit(nopython=True)
def eliminar_ran_hist(img,x1,x2):
    #Eliminar rango de histograma
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            gris =  0.299 * img[i, j, 0] + 0.587 * img[i, j, 1] + 0.114 * img[i, j, 2]
            if gris>=x1 and gris<=x2:
                img[i, j, :] = np.array([0,128,0])
    return img

@jit(nopython=True)

def trasl_ran_hist(img,x1,x2,n1,n2,grises):
    #Eliminar rango de histograma
    c = (n2-n1)/(x2-x1)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            gris =  grises[i,j]
            if np.any((x1 <= gris) & (gris <= x2)):
                r = ((gris-x1)*c+n1)/(gris+1)
                img[i, j, :] *= r
    return img

@jit(nopython=True)
def redim_hist(img,x1,x2,min,max,grises):
    #Redimensionar histograma
    c = (x2-x1)/(max-min)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            gris = grises[i,j]
            ratio = ((gris-min)*c+x1)/(gris+1)
            img[i, j, :] = ratio*img[i, j, :]+1
    return img

@jit(nopython=True)
def bilinear_interpolation(img, ancho1, altura1,result):
    # Obtener el tamaño de imagen
    alto, ancho, channels = img.shape

    # Calcular la razones de escala
    x_r = ancho/ ancho1
    y_r = alto / altura1

    # Para cada pixel de la nueva imagen
    for y in range(altura1):
        for x in range(ancho1):
            # Coordenas en la imagen original
            src_x = x * x_r
            src_y = y * y_r

            # Obtener pixeles vecinos
            x1 = int(src_x)
            y1 = int(src_y)
            x2 = min(x1 + 1, ancho - 1)
            y2 = min(y1 + 1, alto - 1)

            # Calcular coeficientes de interpolación
            alpha = src_x - x1
            beta = src_y - y1

            # Aplicar formula
            for c in range(channels):
                result[y, x, c] = (
                    (1 - alpha) * (1 - beta) * img[y1, x1, c]
                    + alpha * (1 - beta) * img[y1, x2, c]
                    + (1 - alpha) * beta * img[y2, x1, c]
                    + alpha * beta * img[y2, x2, c]
                )

    return result

@jit(nopython=True)
#Ya se tiene la imagen reducida en 100 y con filtro de mediana
def eliminar_rostro(x1,y1,new,img):

    hum = 1600
    x_sup = 0
    y_sup = 0
    x_inf = new.shape[1]-1
    y_inf = new.shape[0]-1

    c = False
    for i in range(x1,new.shape[1]-1):
        #Promedio de la columna
        p_r = np.average(new[y1,x1:i+1,0])
        p_g = np.average(new[y1,x1:i+1,1])
        p_b = np.average(new[y1,x1:i+1,2])
        #Valores en i
        v_r = new[y1,i+1,0]
        v_g = new[y1,i+1,1]
        v_b = new[y1,i+1,2]
        #Diferencia de cuadrados
        d_r = (p_r-v_r)**2
        d_g = (p_g-v_g)**2
        d_b = (p_b-v_b)**2
        d = d_r+d_g+d_b
        #Si la diferencia es mayor a 100
        if d>hum and not c:
            x_inf = i
            c = True
    c = False
    for i in range(y1,new.shape[0]-1):
        #Promedio de la fila
        p_r = np.average(new[y1:i+1,x1,0])
        p_g = np.average(new[y1:i+1,x1,1])
        p_b = np.average(new[y1:i+1,x1,2])
        #Valores en i
        v_r = new[i+1,x1,0]
        v_g = new[i+1,x1,1]
        v_b = new[i+1,x1,2]
        #Diferencia de cuadrados
        d_r = (p_r-v_r)**2
        d_g = (p_g-v_g)**2
        d_b = (p_b-v_b)**2
        d = d_r+d_g+d_b
        #Si la diferencia es mayor a 100
        if d>hum and not c:
            y_inf = i
            c = True
    c = False
    for i in range(x1,0,-1):
        #Promedio de la columna
        p_r = np.average(new[y1,i:x1+1,0])
        p_g = np.average(new[y1,i:x1+1,1])
        p_b = np.average(new[y1,i:x1+1,2])
        #Valores en i
        v_r = new[y1,i-1,0]
        v_g = new[y1,i-1,1]
        v_b = new[y1,i-1,2]
        #Diferencia de cuadrados
        d_r = (p_r-v_r)**2
        d_g = (p_g-v_g)**2
        d_b = (p_b-v_b)**2
        d = d_r+d_g+d_b
        #Si la diferencia es mayor a 100
        if d>hum and not c:
            x_sup = i
            c = True
    c = False 
    for i in range(y1,0,-1):
        #Promedio de la fila
        p_r = np.average(new[i:y1+1,x1,0])
        p_g = np.average(new[i:y1+1,x1,1])
        p_b = np.average(new[i:y1+1,x1,2])
        #Valores en i
        v_r = new[i-1,x1,0]
        v_g = new[i-1,x1,1]
        v_b = new[i-1,x1,2]
        #Diferencia de cuadrados
        d_r = (p_r-v_r)**2
        d_g = (p_g-v_g)**2
        d_b = (p_b-v_b)**2
        d = d_r+d_g+d_b
        #Usando una razón para valores bajos
        if d>hum and not c:
            y_sup = i
            c = True
    
    img[10*y_sup:10*y_inf,10*x_sup:10*x_inf,:] = np.array([0,128,0]) 
    return img

@jit(nopython=True)
def histograma_hexa(img):
    hist = np.zeros(256).astype(np.int32)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):
                a = img[i, j, k]
                hist[a] += 1
    return hist

