#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 12 16:13:44 2024

@author: daniel
"""
from .variables import *
import re
# Direccionamientos considerados dentro de paréntiesis cuadrados
class Fase1:
    def __init__(self):
        #Establece el contenido correcto en el método abrir
        with open('.tmp/000.txt','r') as ens:
            self.__contenido = ens.read()
        #Inicializa con encabezado el texto
        self.__terminos = '0\tfase1\n'
      
    def identificar_tipo_comp(self,arg):
        #Mayúscula = Minúscula, evita confusión
        args = arg.lower()
        #Por default es erróneo
        tipo = 'error'
        #Identifica por medio de expresiones regulares si es compuesto
        cond_dup = re.match(r'dup\s*\([^\)]*\)', args)
        cond_ptr = re.match(r'word\s\s*ptr\s*\[[^\]]*\]|byte\s\s*ptr\s*\[[^\]]*\]',args)
        #Identifica que tipo de dupla es y si su argumento es correcto
        if cond_dup:
            tipo = 'dupla'
            interno = re.findall(r'\((.*?)\)',args)[0]
            tipo += f' tipo {self.identificar_tipo_inm(interno)}'
        #Identifica si el acceso es word o byte
        elif cond_ptr:
            if 'byte' in args:
                tipo = 'direccionamiento byte bd'
            else:
                tipo = 'direccionamiento word dw'
        #Si es un direccionamiento simple
        elif args.endswith(']') and args.startswith('['):
            tipo
            tipo = 'direccionamiento'
        #Si es etiqueta declarada
        elif args.endswith(':') and  re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', args[:-1]):
            tipo = 'etiqueta declarada'
        #Si es simbolo correcto
        elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', args):
            tipo = 'simbolo'
        return 'compuesto ' + tipo

    def identificar_tipo_inm(self,arg):
        #Es erróneo por default
        tipo = 'error'
        #Mayúscula = Minúscula
        args = arg.lower()
        #Recorta espacio al inicio y al final
        args = args.strip()
        #Casting de cadena decimal 
        try:
            s= int(args)
            tipo = 'constante numérica decimal'
            if abs(s)<65536 and abs(s)>=256:
                tipo += ' word dw'
            elif abs(s)<256:
                tipo += ' byte db a dw'
            if s<0:
                tipo += ' con signo'     
        except:
            pass
        #Casting a binario (Si termina en 'b')
        if args.endswith('b'):
            try:
                s=int(args[:-1],2)
                if len(args[:-1])<=8:
                    tipo = 'constante numérica binario byte db a dw'
                elif len(args[:-1])<=16:
                    tipo = 'constante numérica binario word dw'
                if s<0:
                    tipo += ' con signo'
            except:
                pass
        #Casting a hexadecimal (Si inicia en 0 y termina en h, sólo digitos pares)
        if args.endswith('h') and args.startswith('0'):
            try:
                s = int(args[1:-1],16)
                if len(args[1:-1])==2:
                    tipo = 'constante numérica hexadecimal byte db a dw'
                elif len(args[1:-1])==4:
                    tipo = 'constante numérica hexadecimal word dw'
                if s<0:
                    tipo += ' con signo'
            except:
                pass
        #Entre comillas simples/dobles
        if (args.endswith('"') and args.startswith('"')) or (args.endswith("'") and args.startswith("'")):
            tipo = 'constante letra'
            if len(args[1:-1])==1:
                tipo += ' caracter byte db a dw'
            elif len(args[1:-1])==2:
                tipo += 'doble letra word dw'
            elif len(args[1:-1])>2:
                tipo += ' cadena'
        return 'inmediato ' + tipo
    
    def identificar_tipo_res(self,args):
        #Identifica si es una simbolo especial (reservado)
        tipo = 'error'
        args_aux = args.upper()
        if args_aux in reg_gral_16:
            tipo = 'registro general 16bits dw'
        elif args_aux in reg_gral_8:
            tipo = 'registro general 8bits db'
        elif args_aux in reg_base:
            tipo = 'registro  de base dw'
        elif args_aux in reg_index:
            tipo = 'registro de ínidice dw'
        elif args_aux in reg_segmento:
            tipo = 'registro de segmento dw'
        elif args_aux in inst_0:
            tipo = 'instrucción 0 ops.'
        elif args_aux in inst_1:
            tipo = 'instrucción 1 op.'
        elif args_aux in inst_2:
            tipo = 'instrucción 2 ops.'
        elif args_aux == 'DB':
            tipo = 'pseudoinstrucción byte db'
        elif args_aux == 'DW':
            tipo = 'pseudoinstrucción word dw'
        elif args_aux == 'EQU':
            tipo = 'pseudoinstrucción word constante equ'
        elif args_aux == 'DATA':
            tipo = 'segmento de datos con DATA'
            
        return tipo
    
    def identificar_tipo(self,linea):
        tipo = 'error'
        completo = ''
        self.__n += 1
        m = 1
        
        if linea in ps_seg:
            #Si es pseudoinstrucción de segmento
            for ps in ps_seg:
                if ps == linea:
                    tipo = 'pseudoinstrucción segmento'
                    completo += f'{self.__n}.{m}\t{linea}\t#{tipo}\n' 
        elif linea == 'ends':
            #Si es ends
            tipo = 'pseudoinstrucción fin segmento'
            completo += f'{self.__n}.{m}\t{linea}\t#{tipo}\n'     
        else:
            #El patrón separa con expresión regular comas,espacios y tab's
            #Ignora todo lo que esté entre comillas, paréntesis cuadrados (ptr), y dup(...)
            patron = r'(?:"[^"]*"|\'[^\']*\'|\[[^\]]*\]|word\s*ptr\s*\[[^\]]*\]|byte\s*ptr\s*\[[^\]]*\]|dup\s*\([^\)]*\)|[^,\s]+)'
            aux = re.findall(patron, linea.lower())
            for arg in aux:
                tipo = self.identificar_tipo_inm(arg)
                if 'error' in tipo:
                    tipo = self.identificar_tipo_res(arg)
                if 'error' in tipo:
                    tipo = self.identificar_tipo_comp(arg)
                #Linea completa con índice y subíndice
                completo += f'{self.__n}.{m}\t{arg}\t#{tipo}\n'
                m += 1
        return completo
    
    def clasificar_t(self):
        #número de líneas en 0
        self.__n = 0
        #Arreglo de lineas
        lineas = self.__contenido.split('\n')
        #Procesa linea y encuentra el punto donde empieza la linea (No el número)
        for linea in lineas[1:]:
            i =linea.find('\t')+1
            linea_aux = linea[i:]
            #Añade a los términos el tipo
            self.__terminos += f'{self.identificar_tipo(linea_aux)}'
        #Escribe el contenido en el documento temporal
        with open('.tmp/001.txt','w') as fase1:
            fase1.write(self.__terminos)
            
        