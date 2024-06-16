#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 17:18:25 2024

@author: daniel
"""

#Número 3  que decodifica

# Path: modelo/fase3.py

#Se tienen direccionamientos [inm] y [reg]
class Decodificador:
    def __init__(self, fase2):
        self.__fase2 = fase2

    #Instrucciones de un operando
    #Por default se regresa correcto, si no hay operando.
    def aad(self):
        return [2,'','0D50Ah','correcto']
    def aam(self):
        return [2,'','0D40Ah','correcto']
    def cmpsb(self):
        return [1,'','0A6h','correcto']
    def nop(self):  
        return [1,'','090h','correcto']
    def cmc(self):  
        return [1,'','0F5h','correcto']
    def popa(self): 
        return [1,'','061h','correcto']
    
    def buscar_simbolo(self,simbolo):
        ind_var = self.__fase2.get_vars()
        for i in range(len(ind_var)):
            if ind_var[i] == simbolo:
                return self.__fase2.get_tabla()[i]
        return None
    
    def buscar_etq(self,etiqueta):
        ind_etq = self.__fase2.get_etqs()
        for i in range(len(ind_etq)):
            if ind_etq[i] == etiqueta:
                return self.__fase2.get_tabla()[i+len(self.__fase2.get_vars())]
        return None


    #Instrucciones de un operando
    #De etiquetas o salto
    #Correcto si hay etiqueta definida
    #Recive un arreglo arg1 con descripción en [1]
    def ja(self,arg1):
        #Si es simbolo
        if 'simbolo' in arg1[1]:
            desp = self.buscar_etq(arg1[0])
            if desp == None:
                return [0,'','N/A','Error etiqueta no definida']
            else:

                dir = int(desp[0],16) - self.__fase2.get_cont()
                #Si no es menor que -128
                if dir > -129 and dir < 0:
                    #Solo negativos
                    dir = 256 + dir
                    dir = format(dir,'02X')
                    return [2,'',f'077{dir}h','correcto']
                else:
                    return [0,'','N/A','Error en salto mayor a 128']
        else:
            return [0,'','N/A','Error no es simbolo']
        
    def jc(self,arg1):
        #Si es simbolo
        if 'simbolo' in arg1[1]:
            desp = self.buscar_etq(arg1[0])
            if desp == None:
                return [0,'','N/A','Error etiqueta no definida']
            else:

                dir = int(desp[0],16) - self.__fase2.get_cont()
                #Si no es menor que -128
                if dir > -129 and dir < 0:
                    #Solo negativos
                    dir = 256 + dir
                    dir = format(dir,'02X')
                    return [2,'',f'072{dir}h','correcto']
                else:
                    return [0,'','N/A','Error en salto mayor a 128']
        else:
            return [0,'','N/A','Error no es simbolo']

    def jnae(self,arg1):
        #Si es simbolo
        if 'simbolo' in arg1[1]:
            desp = self.buscar_etq(arg1[0])
            if desp == None:
                return [0,'','N/A','Error etiqueta no definida']
            else:

                dir = int(desp[0],16) - self.__fase2.get_cont()
                #Si no es menor que -128
                if dir > -129 and dir < 0:
                    #Solo negativos
                    dir = 256 + dir
                    dir = format(dir,'02X')
                    return [2,'',f'072{dir}h','correcto']
                else:
                    return [0,'','N/A','Error en salto mayor a 128']
        else:
            return [0,'','N/A','Error no es simbolo']
        
    def jnle(self,arg1):

        #Si es simbolo
        if 'simbolo' in arg1[1]:
            desp = self.buscar_etq(arg1[0])
            if desp == None:
                return [0,'','N/A','Error etiqueta no definida']
            else:

                dir = int(desp[0],16) - self.__fase2.get_cont()
                #Si no es menor que -128
                if dir > -129 and dir < 0:
                    #Solo negativos
                    dir = 256 + dir
                    dir = format(dir,'02X')
                    return [2,'',f'07F{dir}h','correcto']
                else:
                    return [0,'','N/A','Error en salto mayor a 128']
        else:
            return [0,'','N/A','Error no es simbolo']
    def jne(self,arg1):
        #Si es simbolo
        if 'simbolo' in arg1[1]:
            desp = self.buscar_etq(arg1[0])
            if desp == None:
                return [0,'','N/A','Error etiqueta no definida']
            else:

                dir = int(desp[0],16) - self.__fase2.get_cont()
                #Si no es menor que -128
                if dir > -129 and dir < 0:
                    #Solo negativos
                    dir = 256 + dir
                    dir = format(dir,'02X')
                    return [2,'',f'075{dir}h','correcto']
                else:
                    return [0,'','N/A','Error en salto mayor a 128']
        else:
            return [0,'','N/A','Error no es simbolo']
    def loope(self,arg1):
        #Si es simbolo
        if 'simbolo' in arg1[1]:
            desp = self.buscar_etq(arg1[0])
            if desp == None:
                return [0,'','N/A','Error etiqueta no definida']
            else:

                dir = int(desp[0],16) - self.__fase2.get_cont()
                #Si no es menor que -128
                if dir > -129 and dir < 0:
                    #Solo negativos
                    dir = 256 + dir
                    dir = format(dir,'02X')
                    return [2,'',f'0E1{dir}h','correcto']
                else:
                    return [0,'','N/A','Error en salto mayor a 128']
        else:
            return [0,'','N/A','Error no es simbolo']
    #Otros
    #Condición especial
    #REG O MEM
    #1111111w mod 000 r/m 0 a 2
    #Falta direccionamiento, pero es directo
    def inc(self,arg):
        n=0
        #Si es registro
        desp = ''
        c_1 = ''
        c_0 = ''
        if 'registro' in arg[1]:
            n = 2
            #Si es db w=0
            if 'db' in arg[1]:
                c_0 = '0FE'
            #Si es dw w=1
            else:
                c_0 = '0FF'
            #Si es registro lo busca en diccionario
            try:
                modrm = self.__mod_dict[str(arg[0]).upper()]
            #Si no lo encuentra
            except:
                return [0,'','N/A','Error registro no existe']
        elif 'simbolo' in arg[1]:
            n = 4
            modrm = self.__mod_dict['DS']
            desp = self.buscar_simbolo(arg[0])
            if 'db' in desp[2]:
                c_0 = '0FE'
            elif 'dw' in desp[2]:
                c_0 = '0FF'
            else:
                return [0,'','N/A','Error: no es variable']
            
            if desp == None:
                return [0,'','N/A','Error variable no definida']
            else:

                desp = desp[0].upper()
        
        #Convierte a hexadecimal de 2 dígitos 1B
        
        c_1 = f'{modrm[0]}100{modrm[1]}'
        c_1 = format(int(c_1,2),'02X')
        #Regresa la instrucción con o sin desplasamiento

        return [n,'',f'{c_0}{c_1}{desp[2:]}{desp[:2]}h','correcto']
    #REG MEM  
    #Igual que inc (mismo funcionamiento)
    #1111011w mod 111 r/m 0 a 2
    def idiv(self,arg):
        n=0
        #Si es registro
        desp = ''
        c_1 = ''
        c_0 = ''
        if 'registro' in arg[1]:
            n = 2
            #Si es db w=0
            if 'db' in arg[1]:
                c_0 = '0F6'
            #Si es dw w=1
            else:
                c_0 = '0F7'
            #Si es registro lo busca en diccionario
            try:
                modrm = self.__mod_dict[str(arg[0]).upper()]
            #Si no lo encuentra
            except:
                return [0,'','N/A','Error registro inexistente']
        elif 'simbolo' in arg[1]:
            n = 4
            modrm = self.__mod_dict['DS']
            desp = self.buscar_simbolo(arg[0])
            if 'db' in desp[2]:
                c_0 = '0F6'
            elif 'dw' in desp[2]:
                c_0 = '0F7'
            else:
                return [0,'','N/A','Error no es variable']
            
            if desp == None:
                return [0,'','N/A','Error tamaño incompatible']
            else:

                desp = desp[0].upper()
        
        #Convierte a hexadecimal de 2 dígitos 1B
        
        c_1 = f'{modrm[0]}111{modrm[1]}'
        c_1 = format(int(c_1,2),'02X')
        #Regresa la instrucción con o sin desplasamiento

        return [n,'',f'{c_0}{c_1}{desp[2:]}{desp[:2]}h','correcto']
    #inm BYTE    
    def iint(self,arg):
        #Un hexadecimal de 2 dígitos no compuesto (por si es direccionamiento)
        cond  = 'hexadecimal' in arg[1] and 'db' in arg[1] and not 'compuesto' in arg[1]
        if cond:
            #Retorna la instrucción con el inmediato
            return [2,'',f'0CD{arg[0][1:-1]}h','correcto']
        else:
            return [0,'','N/A','Error solo inmediato de 1 byte']
    #REG MEM
    #1111011w mod 100 r/m 0 a 2
    def mul(self,arg):
        n=0
        #Si es registro
        desp = ''
        c_1 = ''
        c_0 = ''
        if 'registro' in arg[1]:
            n = 2
            #Si es db w=0
            if 'db' in arg[1]:
                c_0 = '0F6'
            #Si es dw w=1
            else:
                c_0 = '0F7'
            #Si es registro lo busca en diccionario
            try:
                modrm = self.__mod_dict[str(arg[0]).upper()]
            #Si no lo encuentra
            except:
                return [0,'','N/A','Error registro inexistente']
        elif 'simbolo' in arg[1]:
            n = 4
            modrm = self.__mod_dict['DS']
            desp = self.buscar_simbolo(arg[0])
            if 'db' in desp[2]:
                c_0 = '0F6'
            elif 'dw' in desp[2]:
                c_0 = '0F7'
            else:
                return [0,'','N/A','Error no es variable']
            
            if desp == None:
                return [0,'','N/A','Error variable no definida']
            else:

                desp = desp[0].upper()
        
        #Convierte a hexadecimal de 2 dígitos 1B
        
        c_1 = f'{modrm[0]}100{modrm[1]}'
        c_1 = format(int(c_1,2),'02X')
        #Regresa la instrucción con o sin desplasamiento

        return [n,'',f'{c_0}{c_1}{desp[2:]}{desp[:2]}h','correcto']


    #Instrucciones de dos operandos
    #No se tiene mem/mem ni inm/inm



    def convertir_a_hex(self,valor):
        #Ya están verificados por la fase 1
        if valor.startswith('0') and valor.endswith('h'):
            n = int(valor[1:-1],16)
        elif valor.endswith('b'):
            n = int(valor[:-1],2)
        else:
            n = int(valor)
        #Intenta convertir a db
        try :
            return format(n,'02X')
        #Si no se puede es dw forzoso
        except:
            return format(n,'04X')
    '''
    1. REG, memory
    2. memory, REG
    3. REG, REG
    4. memory, immediate
    5. REG, immediate
    '''
    def xor(self,arg1,arg2):
        #'''
        #Registro , registro,memoria,inmediato o constante
        #Si es registro en arg1
        if 'registro' in arg1[1]:
            #Si es registro en arg2 reg-reg
            #Se toma d=0 reg es fuente y  modrm es destino

            if 'inmediato' in arg2[1]:
                #1000 000w mod 110 r/m 0 a 2
                l = self.convertir_a_hex(arg2[0])
                cond = len(l) == 2 and 'db' in arg1[1]
                cond2 = 'dw' in arg1[1]
                if cond:
                    #W=0
                    c_0 = '80'
                    #Fuente
                    #Destino
                    modrm = self.__mod_dict[arg1[0].upper()]
                    c_1 = f'{modrm[0]}110{modrm[1]}'
                    c_1 = format(int(c_1,2),'02X')
                    return [3,'',f'0{c_0}{c_1}{l}h','correcto']
                elif cond2:
                    #W=1
                    #Convierte a hexadecimal de 4 dígitos 2B
                    l = format(int(l,16),'04X')
                    c_0 = '81'
                    #Fuente
                    #Destino
                    modrm = self.__mod_dict[arg1[0].upper()]
                    c_1 = f'{modrm[0]}110{modrm[1]}'
                    c_1 = format(int(c_1,2),'02X')
                    return [4,'',f'0{c_0}{c_1}{l[2:]}{l[:2]}h','correcto']

            elif 'registro' in arg2[1]:
                #0011 000w mod reg r/m 0 a 2
                #Emu toma como d = 1
                cond = 'dw' in arg1[1] and 'dw' in arg2[1]
                cond2 = 'db' in arg1[1] and 'db' in arg2[1]
                if cond:
                    #W=1
                    c_0 = '33'
                    #Fuente
                    reg = self.__regs_dict[arg1[0].upper()]
                    #Destino
                    modrm = self.__mod_dict[arg2[0].upper()]
                    c_1 = f'{modrm[0]}{reg}{modrm[1]}'
                    c_1 = format(int(c_1,2),'02X')
                    return [2,'',f'0{c_0}{c_1}h','correcto']
                elif cond2:
                    #W=0
                    c_0 = '32'
                    #Fuente
                    reg = self.__regs_dict[arg1[0].upper()]
                    #Destino
                    modrm = self.__mod_dict[arg2[0].upper()]
                    c_1 = f'{modrm[0]}{reg}{modrm[1]}'
                    c_1 = format(int(c_1,2),'02X')
                    return [2,'',f'0{c_0}{c_1}h','correcto']
                else:
                    return [0,'','N/A','Error de tamaño incompatible']
            
            #Si es memoria o constante
            elif 'simbolo' in arg2[1]:
               #Si es variable o constante
                desp = self.buscar_simbolo(arg2[0])
                #0011 001w mod reg r/m 0 a 2
                if desp == None:
                    return [0,'','N/A','Error variable']
                #Si es variable reg-mem
                elif desp[2] == 'dw' or desp[2] == 'db':
                    cond = 'dw' in arg1[1] and 'dw' in desp[2]
                    cond2 = 'db' in arg1[1] and 'db' in desp[2]

                    if cond:
                        #W=1
                        c_0 = '33'
                        reg = self.__regs_dict[arg1[0].upper()]
                        modrm = self.__mod_dict['DS']
                        desp = desp[0].upper()
                        c_1 = f'{modrm[0]}{reg}{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                        return [4,'',f'0{c_0}{c_1}{desp[2:]}{desp[:2]}h','correcto'] 
                    
                    elif cond2:
                        #W=0
                        c_0 = '32'
                        reg = self.__regs_dict[arg1[0].upper()]
                        modrm = self.__mod_dict['DS']
                        desp = desp[0].upper()
                        c_1 = f'{modrm[0]}{reg}{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                        return [4,'',f'0{c_0}{c_1}{desp[2:]}{desp[:2]}h','correcto']
                    
                    else:
                        return [0,'','N/A','Error de tamaño incompatible']
                   
                #Si es constante reg- inm
                elif 'equ' in desp[2]:
                    
                    #'''
                    #Llama obtener el valor de la constante
                    #1000 000w mod 110 r/m 0 a 2
                    l = self.convertir_a_hex(desp[4])
                    #'''
                    cond = 'db' in arg1[1] and len(l) == 2
                    cond2 = 'dw' in arg1[1]
                    
                    #'''
                    if cond:
                        #W=0
                        c_0 = '80'
                        #Destino
                        modrm = self.__mod_dict[arg1[0].upper()]
                        c_1 = f'{modrm[0]}110{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                        return [3,'',f'0{c_0}{c_1}{l}h','correcto']
                    elif cond2:
                        #W=1
                        #Convierte a hexadecimal de 4 dígitos 2B
                        l = format(int(l,16),'04X')
                        c_0 = '81'
                        #Destino
                        modrm = self.__mod_dict[arg1[0].upper()]
                        c_1 = f'{modrm[0]}110{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                    #'''
                        return [4,'',f'0{c_0}{c_1}{l[2:]}{l[:2]}h','correcto']
                    else:
                        return [0,'','N/A','Error de tamaño incompatible']
                    #'''
                
            else:
                return [0,'','N/A','Error de registro']
        
        elif 'simbolo' in arg1[1]:
            #Si es variable o constante o inmediato
            desp = self.buscar_simbolo(arg1[0])
            #'''
            if desp == None:
                return [0,'','N/A','Error variable no definida']
            #Si es variable
            elif desp[2] == 'dw' or desp[2] == 'db':
                #Si es variable mem-reg 
                if 'registro' in arg2[1]:
                    #0011 000w mod reg r/m 0 a 2
                    #Comprueba si es registro y valor válido
                    cond = 'dw' in arg2[1] and 'dw' in desp[2]
                    cond2 = 'db' in arg2[1] and 'db' in desp[2]
                    if cond:
                        #W=1
                        c_0 = '31'
                        #Fuente
                        reg = self.__regs_dict[arg2[0].upper()]
                        #Destino
                        modrm = self.__mod_dict['DS']
                        c_1 = f'{modrm[0]}{reg}{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                        return [4,'',f'0{c_0}{c_1}{desp[0][2:]}{desp[0][:2]}h','correcto']
                    elif cond2:
                        #W=0
                        c_0 = '30'
                        #Fuente
                        reg = self.__regs_dict[arg2[0].upper()]
                        #Destino
                        modrm = self.__mod_dict['DS']
                        c_1 = f'{modrm[0]}{reg}{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                        return [4,'',f'0{c_0}{c_1}{desp[0][2:]}{desp[0][:2]}h','correcto'] 

                elif 'simbolo' in arg2[1]:
                    const = self.buscar_simbolo(arg2[0])
                    if const == None:
                        return [0,'','N/A','Error variable no definida']
                    #Si es variable mem-mem no se puede :(
                    elif const[2] == 'dw' or const[2] == 'db':
                        return [0,'','N/A','Error de memoria a memoria'] 
                    #Si es constante mem-inm, se obtiene el valor
                    elif const[2] == 'equ':
                        # 1000 000w mod 110 r/m 0 a 2
                        #Busca el valor de la constante
                        #Convierte en hexadecimal
                        inm = self.convertir_a_hex(const[4])
                        cond = 'db' in desp[2] and len(inm) == 2
                        cond2 = 'dw' in desp[2]
                        if cond:
                            #W=0
                            c_0 = '80'
                            #Fuente
                            reg = 110
                            #Destino
                            modrm = self.__mod_dict['DS']
                            c_1 = f'{modrm[0]}110{modrm[1]}'
                            c_1 = format(int(c_1,2),'02X')
                            return [5,'',f'0{c_0}{c_1}{desp[0][2:]}{desp[0][:2]}{inm}h','correcto']
                        elif cond2:
                            #W=1
                            #Convierte a hexadecimal de 4 dígitos 2B
                            inm = format(int(inm,16),'04X')
                            c_0 = '81'
                            #Fuente
                            reg = 110
                            #Destino
                            modrm = self.__mod_dict['DS']
                            c_1 = f'{modrm[0]}110{modrm[1]}'
                            c_1 = format(int(c_1,2),'02X')
                            return [6,'',f'0{c_0}{c_1}{desp[0][2:]}{desp[0][:2]}{inm[2:]}{inm[:2]}h','correcto']
                        else:
                            return [0,'','N/A','Error de tamaño incompatible']
                #Si es inmediato mem-inm
                elif 'numérica' in arg2[1]:
                    inm = self.convertir_a_hex(arg2[0])
                    #Busca si es db o dw
                    cond = 'db' in desp[2] and len(inm) == 2
                    cond2 = 'dw' in desp[2]
                    if cond:
                        #W=0
                        c_0 = '80'
                        #Fuente
                        #Destino
                        #Será data directo
                        modrm = self.__mod_dict['DS']
                        c_1 = f'{modrm[0]}110{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                        return [5,'',f'0{c_0}{c_1}{desp[0][2:]}{desp[0][:2]}{inm}h','correcto']
                    elif cond2:
                        #W=1
                        #Convierte a hexadecimal de 4 dígitos 2B
                        inm = format(int(inm,16),'04X')
                        c_0 = '81'
                        #Fuente
                        #Destino
                        #Será data directo
                        modrm = self.__mod_dict['DS']
                        c_1 = f'{modrm[0]}110{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                        return [6,'',f'0{c_0}{c_1}{desp[0][2:]}{desp[0][:2]}{inm[2:]}{inm[:2]}h','correcto']
                    else:
                        return [0,'','N/A','Error de tamaño incompatible']
            #'''
                
            #No hay inmediato como destino
            elif desp[2] == 'equ':
                return [0,'','N/A','Error: inmediato no puede ser destino']
            else:
                return [0,'','N/A','Error de argumentos']
        else:
            return [0,'','N/A','Error de argumentos']
        #Memoria , registro, imediato o constante
    #'''
    def ior(self,arg1,arg2):
        #'''
        #Registro , registro,memoria,inmediato o constante
        #Si es registro en arg1
        if 'registro' in arg1[1]:
            #Si es registro en arg2 reg-reg
            #Se toma d=0 reg es fuente y  modrm es destino

            if 'inmediato' in arg2[1]:
                #1000 000w mod 110 r/m 0 a 2
                l = self.convertir_a_hex(arg2[0])
                cond = len(l) == 2 and 'db' in arg1[1]
                cond2 = 'dw' in arg1[1]
                if cond:
                    #W=0
                    c_0 = '80'
                    #Fuente
                    #Destino
                    modrm = self.__mod_dict[arg1[0].upper()]
                    c_1 = f'{modrm[0]}001{modrm[1]}'
                    c_1 = format(int(c_1,2),'02X')
                    return [3,'',f'0{c_0}{c_1}{l}h','correcto']
                elif cond2:
                    #W=1
                    #Convierte a hexadecimal de 4 dígitos 2B
                    l = format(int(l,16),'04X')
                    c_0 = '81'
                    #Fuente
                    #Destino
                    modrm = self.__mod_dict[arg1[0].upper()]
                    c_1 = f'{modrm[0]}001{modrm[1]}'
                    c_1 = format(int(c_1,2),'02X')
                    return [4,'',f'0{c_0}{c_1}{l[2:]}{l[:2]}h','correcto']

            elif 'registro' in arg2[1]:
                #0011 000w mod reg r/m 0 a 2
                #Emu toma como d = 1
                cond = 'dw' in arg1[1] and 'dw' in arg2[1]
                cond2 = 'db' in arg1[1] and 'db' in arg2[1]
                if cond:
                    #W=1
                    c_0 = '0B'
                    #Fuente
                    reg = self.__regs_dict[arg1[0].upper()]
                    #Destino
                    modrm = self.__mod_dict[arg2[0].upper()]
                    c_1 = f'{modrm[0]}{reg}{modrm[1]}'
                    c_1 = format(int(c_1,2),'02X')
                    return [2,'',f'0{c_0}{c_1}h','correcto']
                elif cond2:
                    #W=0
                    c_0 = '0A'
                    #Fuente
                    reg = self.__regs_dict[arg1[0].upper()]
                    #Destino
                    modrm = self.__mod_dict[arg2[0].upper()]
                    c_1 = f'{modrm[0]}{reg}{modrm[1]}'
                    c_1 = format(int(c_1,2),'02X')
                    return [2,'',f'0{c_0}{c_1}h','correcto']
                else:
                    return [0,'','N/A','Error de tamaño incompatible']
            
            #Si es memoria o constante
            elif 'simbolo' in arg2[1]:
               #Si es variable o constante
                desp = self.buscar_simbolo(arg2[0])
                #0011 001w mod reg r/m 0 a 2
                if desp == None:
                    return [0,'','N/A','Error variable no definida']
                #Si es variable reg-mem
                elif desp[2] == 'dw' or desp[2] == 'db':
                    cond = 'dw' in arg1[1] and 'dw' in desp[2]
                    cond2 = 'db' in arg1[1] and 'db' in desp[2]

                    if cond:
                        #W=1
                        c_0 = '0B'
                        reg = self.__regs_dict[arg1[0].upper()]
                        modrm = self.__mod_dict['DS']
                        desp = desp[0].upper()
                        c_1 = f'{modrm[0]}{reg}{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                        return [4,'',f'0{c_0}{c_1}{desp[2:]}{desp[:2]}h','correcto'] 
                    
                    elif cond2:
                        #W=0
                        c_0 = '0A'
                        reg = self.__regs_dict[arg1[0].upper()]
                        modrm = self.__mod_dict['DS']
                        desp = desp[0].upper()
                        c_1 = f'{modrm[0]}{reg}{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                        return [4,'',f'0{c_0}{c_1}{desp[2:]}{desp[:2]}h','correcto']
                    
                    else:
                        return [0,'','N/A','Error de tamaño incompatible']
                   
                #Si es constante reg- inm
                elif 'equ' in desp[2]:
                    
                    #'''
                    #Llama obtener el valor de la constante
                    #1000 000w mod 110 r/m 0 a 2
                    l = self.convertir_a_hex(desp[4])
                    #'''
                    cond = 'db' in arg1[1] and len(l) == 2
                    cond2 = 'dw' in arg1[1]
                    
                    #'''
                    if cond:
                        #W=0
                        c_0 = '80'
                        #Destino
                        modrm = self.__mod_dict[arg1[0].upper()]
                        c_1 = f'{modrm[0]}001{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                        return [3,'',f'0{c_0}{c_1}{l}h','correcto']
                    elif cond2:
                        #W=1
                        #Convierte a hexadecimal de 4 dígitos 2B
                        l = format(int(l,16),'04X')
                        c_0 = '81'
                        #Destino
                        modrm = self.__mod_dict[arg1[0].upper()]
                        c_1 = f'{modrm[0]}001{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                    #'''
                        return [4,'',f'0{c_0}{c_1}{l[2:]}{l[:2]}h','correcto']
                    else:
                        return [0,'','N/A','Error de tamaño incompatible']
                    #'''
                
            else:
                return [0,'','N/A','Error de registro']
        
        elif 'simbolo' in arg1[1]:
            #Si es variable o constante o inmediato
            desp = self.buscar_simbolo(arg1[0])
            #'''
            if desp == None:
                return [0,'','N/A','Error variable']
            #Si es variable
            elif desp[2] == 'dw' or desp[2] == 'db':
                #Si es variable mem-reg 
                if 'registro' in arg2[1]:
                    #0011 000w mod reg r/m 0 a 2
                    #Comprueba si es registro y valor válido
                    cond = 'dw' in arg2[1] and 'dw' in desp[2]
                    cond2 = 'db' in arg2[1] and 'db' in desp[2]
                    if cond:
                        #W=1
                        c_0 = '81'
                        #Fuente
                        reg = self.__regs_dict[arg2[0].upper()]
                        #Destino
                        modrm = self.__mod_dict['DS']
                        c_1 = f'{modrm[0]}{reg}{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                        return [4,'',f'0{c_0}{c_1}{desp[0][2:]}{desp[0][:2]}h','correcto']
                    elif cond2:
                        #W=0
                        c_0 = '80'
                        #Fuente
                        reg = self.__regs_dict[arg2[0].upper()]
                        #Destino
                        modrm = self.__mod_dict['DS']
                        c_1 = f'{modrm[0]}{reg}{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                        return [4,'',f'0{c_0}{c_1}{desp[0][2:]}{desp[0][:2]}h','correcto'] 

                elif 'simbolo' in arg2[1]:
                    const = self.buscar_simbolo(arg2[0])
                    if const == None:
                        return [0,'','N/A','Error variable indeterminada']
                    #Si es variable mem-mem no se puede :(
                    elif const[2] == 'dw' or const[2] == 'db':
                        return [0,'','N/A','Error memoria a memoria no permitido']
                    #Si es constante mem-inm, se obtiene el valor
                    elif const[2] == 'equ':
                        # 1000 000w mod 110 r/m 0 a 2
                        #Busca el valor de la constante
                        #Convierte en hexadecimal
                        inm = self.convertir_a_hex(const[4])
                        cond = 'db' in desp[2] and len(inm) == 2
                        cond2 = 'dw' in desp[2]
                        if cond:
                            #W=0
                            c_0 = '80'
                            #Fuente
                            reg = 110
                            #Destino
                            modrm = self.__mod_dict['DS']
                            c_1 = f'{modrm[0]}001{modrm[1]}'
                            c_1 = format(int(c_1,2),'02X')
                            return [5,'',f'0{c_0}{c_1}{desp[0][2:]}{desp[0][:2]}{inm}h','correcto']
                        elif cond2:
                            #W=1
                            #Convierte a hexadecimal de 4 dígitos 2B
                            inm = format(int(inm,16),'04X')
                            c_0 = '81'
                            #Fuente
                            reg = 110
                            #Destino
                            modrm = self.__mod_dict['DS']
                            c_1 = f'{modrm[0]}001{modrm[1]}'
                            c_1 = format(int(c_1,2),'02X')
                            return [6,'',f'0{c_0}{c_1}{desp[0][2:]}{desp[0][:2]}{inm[2:]}{inm[:2]}h','correcto']
                        else:
                            return [0,'','N/A','Error de tamaño incompatible']
                #Si es inmediato mem-inm
                elif 'numérica' in arg2[1]:
                    inm = self.convertir_a_hex(arg2[0])
                    #Busca si es db o dw
                    cond = 'db' in desp[2] and len(inm) == 2
                    cond2 = 'dw' in desp[2]
                    if cond:
                        #W=0
                        c_0 = '80'
                        #Fuente
                        #Destino
                        #Será data directo
                        modrm = self.__mod_dict['DS']
                        c_1 = f'{modrm[0]}001{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                        return [5,'',f'0{c_0}{c_1}{desp[0][2:]}{desp[0][:2]}{inm}h','correcto']
                    elif cond2:
                        #W=1
                        #Convierte a hexadecimal de 4 dígitos 2B
                        inm = format(int(inm,16),'04X')
                        c_0 = '81'
                        #Fuente
                        #Destino
                        #Será data directo
                        modrm = self.__mod_dict['DS']
                        c_1 = f'{modrm[0]}001{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                        return [6,'',f'0{c_0}{c_1}{desp[0][2:]}{desp[0][:2]}{inm[2:]}{inm[:2]}h','correcto']
                    else:
                        return [0,'','N/A','Error de tamaño incompatible']
            #'''
                
            #No hay inmediato como destino
            elif desp[2] == 'equ':
                return [0,'','N/A','Error: inmediato como destino no permitido']
            else:
                return [0,'','N/A','Error de argumentos']
        else:
            return [0,'','N/A','Error de argumentos']
    def iand(self,arg1,arg2):
        #'''
        #Registro , registro,memoria,inmediato o constante
        #Si es registro en arg1
        if 'registro' in arg1[1]:
            #Si es registro en arg2 reg-reg
            #Se toma d=0 reg es fuente y  modrm es destino

            if 'inmediato' in arg2[1]:
                #1000 000w mod 100 r/m 0 a 2
                l = self.convertir_a_hex(arg2[0])
                cond = len(l) == 2 and 'db' in arg1[1]
                cond2 = 'dw' in arg1[1]
                if cond:
                    #W=0
                    c_0 = '80'
                    #Fuente
                    reg = 110
                    #Destino
                    modrm = self.__mod_dict[arg1[0].upper()]
                    c_1 = f'{modrm[0]}100{modrm[1]}'
                    c_1 = format(int(c_1,2),'02X')
                    return [3,'',f'0{c_0}{c_1}{l}h','correcto']
                elif cond2:
                    #W=1
                    #Convierte a hexadecimal de 4 dígitos 2B
                    l = format(int(l,16),'04X')
                    c_0 = '81'
                    #Fuente
                    reg = 110
                    #Destino
                    modrm = self.__mod_dict[arg1[0].upper()]
                    c_1 = f'{modrm[0]}100{modrm[1]}'
                    c_1 = format(int(c_1,2),'02X')
                    return [4,'',f'0{c_0}{c_1}{l[2:]}{l[:2]}h','correcto']

            elif 'registro' in arg2[1]:
                #0011 000w mod reg r/m 0 a 2
                #Emu toma como d = 1
                cond = 'dw' in arg1[1] and 'dw' in arg2[1]
                cond2 = 'db' in arg1[1] and 'db' in arg2[1]
                if cond:
                    #W=1
                    c_0 = '23'
                    #Fuente
                    reg = self.__regs_dict[arg1[0].upper()]
                    #Destino
                    modrm = self.__mod_dict[arg2[0].upper()]
                    c_1 = f'{modrm[0]}{reg}{modrm[1]}'
                    c_1 = format(int(c_1,2),'02X')
                    return [2,'',f'0{c_0}{c_1}h','correcto']
                elif cond2:
                    #W=0
                    c_0 = '22'
                    #Fuente
                    reg = self.__regs_dict[arg1[0].upper()]
                    #Destino
                    modrm = self.__mod_dict[arg2[0].upper()]
                    c_1 = f'{modrm[0]}{reg}{modrm[1]}'
                    c_1 = format(int(c_1,2),'02X')
                    return [2,'',f'0{c_0}{c_1}h','correcto']
                else:
                    return [0,'','N/A','Error de tamaño incompartible']
            
            #Si es memoria o constante
            elif 'simbolo' in arg2[1]:
               #Si es variable o constante
                desp = self.buscar_simbolo(arg2[0])
                #0011 001w mod reg r/m 0 a 2
                if desp == None:
                    return [0,'','N/A','Error variable indefinida']
                #Si es variable reg-mem
                elif desp[2] == 'dw' or desp[2] == 'db':
                    cond = 'dw' in arg1[1] and 'dw' in desp[2]
                    cond2 = 'db' in arg1[1] and 'db' in desp[2]

                    if cond:
                        #W=1
                        c_0 = '23'
                        reg = self.__regs_dict[arg1[0].upper()]
                        modrm = self.__mod_dict['DS']
                        desp = desp[0].upper()
                        c_1 = f'{modrm[0]}{reg}{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                        return [4,'',f'0{c_0}{c_1}{desp[2:]}{desp[:2]}h','correcto'] 
                    
                    elif cond2:
                        #W=0
                        c_0 = '22'
                        reg = self.__regs_dict[arg1[0].upper()]
                        modrm = self.__mod_dict['DS']
                        desp = desp[0].upper()
                        c_1 = f'{modrm[0]}{reg}{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                        return [4,'',f'0{c_0}{c_1}{desp[2:]}{desp[:2]}h','correcto']
                    
                    else:
                        return [0,'','N/A','Error de tamaño incompartible']
                   
                #Si es constante reg- inm
                elif 'equ' in desp[2]:
                    
                    #'''
                    #Llama obtener el valor de la constante
                    #1000 000w mod 110 r/m 0 a 2
                    l = self.convertir_a_hex(desp[4])
                    #'''
                    cond = 'db' in arg1[1] and len(l) == 2
                    cond2 = 'dw' in arg1[1]
                    
                    #'''
                    if cond:
                        #W=0
                        c_0 = '80'
                        #Destino
                        modrm = self.__mod_dict[arg1[0].upper()]
                        c_1 = f'{modrm[0]}100{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                        return [3,'',f'0{c_0}{c_1}{l}h','correcto']
                    elif cond2:
                        #W=1
                        #Convierte a hexadecimal de 4 dígitos 2B
                        l = format(int(l,16),'04X')
                        c_0 = '81'
                        #Destino
                        modrm = self.__mod_dict[arg1[0].upper()]
                        c_1 = f'{modrm[0]}100{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                    #'''
                        return [4,'',f'0{c_0}{c_1}{l[2:]}{l[:2]}h','correcto']
                    else:
                        return [0,'','N/A','Error de tamaño incompartible']
                    #'''
                
            else:
                return [0,'','N/A','Error de registro inconrrecto']
        
        elif 'simbolo' in arg1[1]:
            #Si es variable o constante o inmediato
            desp = self.buscar_simbolo(arg1[0])
            #'''
            if desp == None:
                return [0,'','N/A','Error variable indefinida']
            #Si es variable
            elif desp[2] == 'dw' or desp[2] == 'db':
                #Si es variable mem-reg 
                if 'registro' in arg2[1]:
                    #0011 000w mod reg r/m 0 a 2
                    #Comprueba si es registro y valor válido
                    cond = 'dw' in arg2[1] and 'dw' in desp[2]
                    cond2 = 'db' in arg2[1] and 'db' in desp[2]
                    if cond:
                        #W=1
                        c_0 = '21'
                        #Fuente
                        reg = self.__regs_dict[arg2[0].upper()]
                        #Destino
                        modrm = self.__mod_dict['DS']
                        c_1 = f'{modrm[0]}{reg}{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                        return [4,'',f'0{c_0}{c_1}{desp[0][2:]}{desp[0][:2]}h','correcto']
                    elif cond2:
                        #W=0
                        c_0 = '20'
                        #Fuente
                        reg = self.__regs_dict[arg2[0].upper()]
                        #Destino
                        modrm = self.__mod_dict['DS']
                        c_1 = f'{modrm[0]}{reg}{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                        return [4,'',f'0{c_0}{c_1}{desp[0][2:]}{desp[0][:2]}h','correcto'] 

                elif 'simbolo' in arg2[1]:
                    const = self.buscar_simbolo(arg2[0])
                    if const == None:
                        return [0,'','N/A','Error variable indefinida']
                    #Si es variable mem-mem no se puede :(
                    elif const[2] == 'dw' or const[2] == 'db':
                        return [0,'','N/A','Error memoria a memoria no permitido']
                    #Si es constante mem-inm, se obtiene el valor
                    elif const[2] == 'equ':
                        # 1000 000w mod 110 r/m 0 a 2
                        #Busca el valor de la constante
                        #Convierte en hexadecimal
                        inm = self.convertir_a_hex(const[4])
                        cond = 'db' in desp[2] and len(inm) == 2
                        cond2 = 'dw' in desp[2]
                        if cond:
                            #W=0
                            c_0 = '80'
                            #Fuente
                            #Destino
                            modrm = self.__mod_dict['DS']
                            c_1 = f'{modrm[0]}100{modrm[1]}'
                            c_1 = format(int(c_1,2),'02X')
                            return [5,'',f'0{c_0}{c_1}{desp[0][2:]}{desp[0][:2]}{inm}h','correcto']
                        elif cond2:
                            #W=1
                            #Convierte a hexadecimal de 4 dígitos 2B
                            inm = format(int(inm,16),'04X')
                            c_0 = '81'
                            #Fuente
                            #Destino
                            modrm = self.__mod_dict['DS']
                            c_1 = f'{modrm[0]}100{modrm[1]}'
                            c_1 = format(int(c_1,2),'02X')
                            return [6,'',f'0{c_0}{c_1}{desp[0][2:]}{desp[0][:2]}{inm[2:]}{inm[:2]}h','correcto']
                        else:
                            return [0,'','N/A','Error de tamaño incompatible']
                #Si es inmediato mem-inm
                elif 'numérica' in arg2[1]:
                    inm = self.convertir_a_hex(arg2[0])
                    #Busca si es db o dw
                    cond = 'db' in desp[2] and len(inm) == 2
                    cond2 = 'dw' in desp[2]
                    if cond:
                        #W=0
                        c_0 = '80'
                        #Fuente
                        #Destino
                        #Será data directo
                        modrm = self.__mod_dict['DS']
                        c_1 = f'{modrm[0]}100{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                        return [5,'',f'0{c_0}{c_1}{desp[0][2:]}{desp[0][:2]}{inm}h','correcto']
                    elif cond2:
                        #W=1
                        #Convierte a hexadecimal de 4 dígitos 2B
                        inm = format(int(inm,16),'04X')
                        c_0 = '81'
                        #Fuente
                        #Destino
                        #Será data directo
                        modrm = self.__mod_dict['DS']
                        c_1 = f'{modrm[0]}100{modrm[1]}'
                        c_1 = format(int(c_1,2),'02X')
                        return [6,'',f'0{c_0}{c_1}{desp[0][2:]}{desp[0][:2]}{inm[2:]}{inm[:2]}h','correcto']
                    else:
                        return [0,'','N/A','Error de tamaño incompatible']
            #'''
                
            #No hay inmediato como destino
            elif desp[2] == 'equ':
                return [0,'','N/A','Error fuente es valor inmediato']
            else:
                return [0,'','N/A','Error de argumentos']
        else:
            return [0,'','N/A','Error de argumentos']
    '''
    REG MEM
    '''
    #Sólo registros y memoria
    def lea(self,arg1,arg2):
       
        if 'simbolo' in arg2[1] and 'registro' in arg1[1] and 'dw' in arg1[1]:
            desp = self.buscar_simbolo(arg2[0])
            if desp == None:
                return [0,'','N/A','Error variable']
            #Se puede leer dirección db o dw en registros, pero completos
            elif desp[2] == 'dw' or desp[2] == 'db':
                modrm = self.__mod_dict['DS']
                desp = desp[0].upper()
                #Convierte a hexadecimal de 2 dígitos 1B
                c_1 = f'{modrm[0]}{self.__regs_dict[arg1[0].upper()]}{modrm[1]}'
                c_1 = format(int(c_1,2),'02X')
                return [4,'',f'08D{c_1}{desp[2:]}{desp[:2]}h','correcto']
        else:
            return [0,'','N/A','Error: solo registro como destino']

    #Principal de variables
    def iniciar(self):
        #Todas las instrucciones asignadas
        self.__dict0 =  {"AAD":self.aad,
                         "AAM":self.aam,
                         "CMPSB":self.cmpsb,
                         "NOP":self.nop,
                         "CMC":self.cmc,
                         "POPA":self.popa}
        
        self.__dict1 = {"JA":self.ja,
                        "JC":self.jc,
                        "JNAE":self.jnae,
                        "JNE":self.jne,
                        "JNLE":self.jnle,
                        "LOOPE":self.loope,
                        "INC":self.inc,
                        #Se agrega i a int porque es palabra reservada
                        "INT":self.iint,
                        "MUL":self.mul,
                        "IDIV":self.idiv}
        
        self.__dict2 = {"XOR":self.xor,
                        #Se agrega i a or porque es palabra reservada
                        "OR":self.ior,
                        #Se agrega i a and porque es palabra reservada
                        "AND":self.iand,
                        "LEA":self.lea}
        
        self.__regs_dict = {"AX":'000',
                            "AL":'000',
                            "CX":'001',
                            "CL":'001',
                            "DX":'010',
                            "DL":'010',
                            "BX": '011',
                            "BL": '011',
                            "SP": '100',
                            "AH": '100',
                            "BP": '101',
                            "CH": '101',
                            "SI": '110',
                            "DH": '110',
                            "DI": '111',
                            "BH": '111'}
        
        self.__mod_dict = { "DS": ['00','110'],
                           "AX":['11','000'],
                           "AL":['11','000'],
                           "CX":['11','001'],
                           "CL":['11','001'],
                           "DX":['11','010'],
                           "DL":['11','010'],
                           "BX":['11', '011'],
                           "BL":['11', '011'],
                           "SP":['11', '100'],
                           "AH":['11', '100'],
                           "BP":['11', '101'],
                           "CH":['11', '101'],
                           "SI":['11', '110'],
                           "DH":['11', '110'],
                           "DI":['11', '111'],
                           "BH":['11', '111']}
        
    #Calcular tamaño de tabla de simbolos
    #Calcular tamaño de tabla de codigos
    #Si es dupla ps*long = tamaño, pero long es valor (No se usa el contenido)
    def calcular_tam_sim(self,ps,tpl,tp,val):
        #No se considera db porque por default es 1
        #cond1 = ps == 'db'
        cond2 = ps == 'dw'
        cond3 = ps == 'equ'
        cond4 = 'dupla' in tp
        #No hay dupla cadena en este punto
        cond5 = 'cadena' in tp
        cond6 = 'hexadecimal' in tpl
        cond7 = 'binario' in tpl
        cond8 = 'decimal' in tpl
        l=1 #Por default
        #Conversión de longitudes
        if cond4:
            if cond6:
                l = int(val.split(' ')[0][:-1],16)
            elif cond7:
                l = int(val.split(' ')[0][:-1],2)
            elif cond8:
                l = int(val.split(' ')[0])
                #print(f'Longitud = {l}')
        if cond5:
            l = len(val)
        #En la fase anterior no se permitiero equ de cadena, asegura que equ = 2B
        if cond2 or cond3:
            l = 2*l
        #print(f'Longitud de {ps} = {l}')
        return l
        

    #Decodificador usa la linea y las tablas actualizadas
    def decodificar(self,linea):
        l = len(linea)
        if l == 1:
            try:
                a = self.__dict0[str(linea[0][0]).upper()]()
                return a
            except:
                return [0,'','N/A','Error: los argumentos no son correctos']
        elif l==2:
            try:
                a = self.__dict1[str(linea[0][0]).upper()](linea[1])
                return a
            except:

                return [0,'','N/A','Error: los argumentos no son correctos']
        elif l==3:
            try:
                a = self.__dict2[str(linea[0][0]).upper()](linea[1],linea[2])
                return a
            
            except:
                return [0,'','N/A','Error: los argumentos no son correctos']
        else:
            return [0,'','N/A','Error: Más de 2 argumentos']
        #Identifica si es una instrucción correcta inst args,*
        #Si no lo es es no identificado
